# Instructions
- build a simple webservice

# Endpoints
- endpoint `health` check if the service is alive
- endpoint `summarize` to create a reviews summary

# Input
```json
{
     "reviews":[
          {"review": <some text>},
          {"review": <some text>}
     ]
}
```

# Output
```json
{
     "summary": <summarized reviews>
}
```