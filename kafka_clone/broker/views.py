from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.db import transaction
import hashlib

class TopicView(APIView):
    def post(self, request):
        name = request.data.get("name")
        partitions = request.data.get("partitions", 3)

        if Topic.objects.filter(topic=name).exists():
            # status 400 is for bad request
            return Response({"error": f"Topic {name} already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # transaction.atomic() is used to ensure that the operations are atomic. atomic operations are operations that are either fully completed or not completed at all.
        with transaction.atomic():
            topic = Topic.objects.create(name=name, partitions=partitions)
            for i in range(partitions):
                Partition.objects.create(topic=topic, partition=i, leader='127.0.0.1')
        return Response({"name": name, 'partitions': partitions}, status=status.HTTP_201_CREATED)


class MessageView(APIView):
    def post(self, request):
        topic_name = request.data.get("topic")
        key = request.data.get("key", "")
        value = request.data.get("value")

        try:
            topic = Topic.objects.get(name=topic_name)
        except Topic.DoesNotExist:
            return Response({"error": f"Topic {topic_name} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # hash(key) % topic.partitions is used to determine the partition number that the message should be written to. The hash function is used to generate a unique identifier for the key, which is then used to determine the partition number. If no key is provided, the default partition number is 0.
        partition_number = hash(key) % topic.partitions if key else 0

        partition = Partition.objects.get(topic=topic, partition_number=partition_number)

        with transaction.atomic():
            # last offset is the offset of the last message in the partition
            last_offset = Message.objects.filter(partition=partition).order_by('-offset').first()
            # new_offset is the offset of the new message
            new_offset = last_offset.offset + 1 if last_offset else 0

            Message.objects.create(partition=partition, offset=new_offset, key=key, value=value)

            return Response({"topic": topic_name, "partition": partition_number, "offset": new_offset}, status=status.HTTP_201_CREATED)

    def get(self, request):
        group_id = request.GET.get('group_id')
        topic_name = request.GET.get('topic')

        try:
            group = ConsumerGroup.objects.get(id=group_id)
            topic = Topic.objects.get(name=topic_name)
        except (ConsumerGroup.DoesNotExist, Topic.DoesNotExist):
            return Response({"error": f"Topic {topic_name} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        messages = []
        for partition in topic.partition_set.all():
            last_offset = group.offsets.get(str(partition.id), 0)
            partition_messages = Message.objects.filter(partition=partition, offset__gt=last_offset).order_by('offset')[:10]

            for msg in partition_messages:
                messages.append({
                    'partition': partition.partition_id,
                    'offset': msg.offset,
                    'key': msg.key,
                    'value': msg.value,
                })
                group.offsets[str(partition.id)] = msg.offset + 1

        group.save()
        return Response(messages if messages else [], status=status.HTTP_200_OK if messages else status.HTTP_204_NO_CONTENT)