from pydantic import BaseModel


class Definitions(BaseModel):
    query: str = (
        "The segment of the transcript that provides background and ongoing conversation leading up to the key statement. It includes all dialogue that sets the stage for what follows."
    )
    optimal: str = (
        "The direct response or reaction following the query. This is the statement that follows the query, formatted with proper speaker tags."
    )


class GenerateCritiqueConfig(BaseModel):
    chunk_size: int = 3500
    chunk_overlap: int = 2500


class GenerateCritiqueInput(BaseModel):
    file_url: str
    config: GenerateCritiqueConfig
    instructions: str = (
        """
# Transcript Structuring Agent Prompt

Your task is to take a snippet from a transcript and convert it into a structured format with two parts: **query**, and **optimal**. Each part must be clearly delineated and formatted exactly as specified. The output should strictly follow the structure provided below.

---

## Instructions

2. **Query**  
   - Capture the conversation that leads up to a particular statement.
   - Include all dialogue preceding the key moment to provide necessary background and situational setup.
   - Use the same speaker formatting as in the transcript (e.g., `**SpeakerName:** Dialogue` separated by new lines).
   - The statement made immediately before the response.
   - Ensure that the exact dialogue is captured with proper speaker tags.

3. **Optimal**  
   - Represent the direct response or reaction following the query.
   - Format the response using the same speaker tags as in the transcript.

---

## Example Format

### Example 1

#### Query
```
**Alex**: Hey Jamie, I'm really craving something Italian tonight. I was thinking of maybe trying that new trattoria downtown.
**Jamie**: Yeah, I've heard great things about it. Their pasta is supposed to be amazing.
**Alex**: Should we make a reservation, or just walk in?
```

#### Optimal
```
**Jamie**: I think we should call ahead to reserve a table since it's likely to be busy on a Friday night.
``` 

---

### Example 2

#### Query
```
**Sarah**: I've been thinking about our upcoming vacation. We have a few options for where to go, like the beach or the mountains.
**Michael**: True, the mountains would offer some nice hiking opportunities and a cooler climate.
**Sarah**: What do you think about booking a cabin in the mountains for the weekend?
```

#### Optimal
```
**Michael**: That sounds like a great idea, especially if we want a break from the city noise and enjoy some fresh air.
```

---

### Example 3

#### Query
```
**Emma**: We have an important meeting with the clients tomorrow, and I think we need to prepare some visuals.
**Liam**: I agree. The presentation could really benefit from some clear charts and graphs.
**Emma**: Do you want me to handle the slide deck while you work on the data analysis?
```

#### Optimal
```
**Liam**: Yes, that works perfectly. I'll finalize the numbers and send them to you by the end of the day.
```

---

### Example 4

#### Query
```
**Chris**: I can't decide what to order from this new burger joint. Everything looks delicious.
**Pat**: I've been here a couple of times, and their special burger is really good.
**Chris**: Would you recommend trying the special burger, or should I stick with a classic cheeseburger?
```

#### Optimal
```
**Pat**: I would definitely go with the special burger. It has a unique twist that you won't find in a typical cheeseburger.
```

---

### Example 5

#### Query
```
**Jordan**: I've been feeling a bit cooped up with all the work lately. Maybe it's time to do something fun over the weekend.
**Taylor**: That sounds like a good idea. We haven't done anything adventurous in a while.
**Jordan**: How about we try that new escape room in the city?
```

#### Optimal
```
**Taylor**: I love that idea! It will be a great challenge and a fun way to spend our weekend.
```

---

Your final output should strictly adhere to this structure. Do not include any additional commentary or formatting beyond the sections specified above.
    """.strip()
    )
    definitions: Definitions


class GenerateCritiqueOutput(BaseModel):
    context: str
    query: str
    optimal: str
    situation: str
