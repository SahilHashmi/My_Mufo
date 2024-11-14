# serializer.py

from rest_framework import serializers
from rest_framework.utils import model_meta
from .models import Room, Chat


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"
        lookup_field = "room_code"
        read_only_fields = ['room_code', 'creator']
        extra_kwargs = {k: {'required': False, 'allow_null': True, 'write_only': True}
                        for k in ['active_bots', 'blocked_users']}

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save(room_code=True)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    def create(self, validated_data):
        room = Room(**validated_data)
        room.save(room_code=False)
        return room


# serializers.py
   
class ChatSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source="from_user.Name")

    class Meta:
        model = Chat 
        fields = '__all__'
        read_only_fields = ['room', 'from_user', 'text']

        extra_kwargs = {k: {'read_only':True} for k in read_only_fields}


# class ChatSerializer(serializers.ModelSerializer):
#     room_name = serializers.CharField(source="room.room_name", read_only=True)

#     class Meta:
#         model = Chat
#         fields = '__all__'

class RoomsGetSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_code', 'room_name', 'creator', 'blocked_users', 'active_bots', 'is_public', 'creator_name', 'creator_profile_picture',
                  'room_Image','room_category']

    def get_creator_name(self, room):
        # Access the creator of the room and return their name
        if room.creator:
            return room.creator.Name
        return None

    def get_creator_profile_picture(self, room):
        # Access the creator of the room and return their profile picture
        if room.creator:
            return room.creator.profile_picture
        return None