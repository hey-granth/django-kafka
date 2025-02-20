from django.db import models
import uuid

class Broker:
    name = models.CharField(max_length=255)

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    partitions = models.PositiveIntegerField(default=3)
    # Replication factor is the number of copies of a topic that are stored on different brokers for fault tolerance
    replication_factor = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Partition(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    partition_id = models.PositiveIntegerField()
    # leader is the broker that is responsible for handling read and write requests for a partition
    leader = models.ForeignKey(Broker, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('topic', 'partition_id')


class Message(models.Model):
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
    # offset is the unique identifier of a message within a partition
    offset = models.PositiveIntegerField()
    # key is an optional field that can be used to store a unique identifier for a message
    key = models.TextField(blank=True, null=True)
    # value is the actual message that is stored in the partition
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ConsumerGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    offsets = models.JSONField(default=dict) # {partition_id: offset}

