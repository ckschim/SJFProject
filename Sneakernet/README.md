# SneakerNet

## commands

```
users.py [-new_name]
  - if necessary, creates and initializes a new local user, prompts for a name
  - lists all known feedIDs and associated names
  - with the option '-new_name', one can change one's own name

dump-log.py [log_file]
  - pretty-prints for each event the sequence number and event body

```

## file conventions

```
MyFeedID.json    private and public key of local user
logs             directory for all (replicated) logs, events must be sorted
logs/1.pcap      log of local user
logs/2 ...       log of other users
```
