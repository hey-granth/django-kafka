# Notes for Self Referencing

## Table of Contents
1. [UUID](##UUID)
2. [Partitions in Kafka](##Partitions-in-Kafka)

## UUID
- Universally Unique Identifier
- 128-bit number identifier, used to prevent conflicts between IDs.
- Safer than integers for IDs (harder to guess, avoids collisions).

## Partitions in Kafka
- Partitions are the way Kafka scales.
- Each partition is an ordered, immutable sequence of records that is continually appended to.
- Each partition has one leader and zero or more followers.
- Basically, a partition is a log, and dividing the whole set of logs into small partitions helps a lot ini parallel processing.
- It becomes easier to scale, and faster to read/write data.

