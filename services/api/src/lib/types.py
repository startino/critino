from pydantic import BaseModel


class Definitions(BaseModel):
    context: str = (
        "The segment of the transcript that provides background and ongoing conversation leading up to the key statement. It includes all dialogue that sets the stage for what follows."
    )
    query: str = (
        "The specific statement made immediately before the response. This part is isolated and represents the dialogue that triggers the following reaction."
    )
    optimal: str = (
        "The direct response or reaction following the query. This is the statement that follows the query, formatted with proper speaker tags."
    )


class GenerateCritiqueConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int


class GenerateCritiqueInput(BaseModel):
    file_url: str
    config: GenerateCritiqueConfig
    instructions: str = (
        """
# Transcript Structuring Agent Prompt

Your task is to take a snippet from a transcript and convert it into a structured format with three parts: **context**, **query**, and **optimal**. Each part must be clearly delineated and formatted exactly as specified. The output should strictly follow the structure provided below.

---

## Instructions

1. **Context**  
   - Capture the conversation that leads up to a particular statement.
   - Include all dialogue preceding the key moment to provide necessary background and situational setup.
   - Use the same speaker formatting as in the transcript (e.g., `<SpeakerName>Dialogue</SpeakerName>`).

2. **Query**  
   - This is the statement made immediately before the response.
   - Isolate this statement from the rest of the conversation.
   - Ensure that the exact dialogue is captured with proper speaker tags.

3. **Optimal**  
   - Represent the direct response or reaction following the query.
   - Format the response using the same speaker tags as in the transcript.

---

## Example Format

### Example 1

#### Context
```
<Alex>Hey Jamie, I'm really craving something Italian tonight. I was thinking of maybe trying that new trattoria downtown.</Alex>
<Jamie>Yeah, I've heard great things about it. Their pasta is supposed to be amazing.</Jamie>
```

#### Query
```
<Alex>Should we make a reservation, or just walk in?</Alex>
```

#### Optimal
```
<Jamie>I think we should call ahead to reserve a table since it's likely to be busy on a Friday night.</Jamie>
``` 

---

### Example 2

#### Context
```
<Sarah>I've been thinking about our upcoming vacation. We have a few options for where to go, like the beach or the mountains.</Sarah>
<Michael>True, the mountains would offer some nice hiking opportunities and a cooler climate.</Michael>
```

#### Query
```
<Sarah>What do you think about booking a cabin in the mountains for the weekend?</Sarah>
```

#### Optimal
```
<Michael>That sounds like a great idea, especially if we want a break from the city noise and enjoy some fresh air.</Michael>
```

---

### Example 3

#### Context
```
<Emma>We have an important meeting with the clients tomorrow, and I think we need to prepare some visuals.</Emma>
<Liam>I agree. The presentation could really benefit from some clear charts and graphs.</Liam>
```

#### Query
```
<Emma>Do you want me to handle the slide deck while you work on the data analysis?</Emma>
```

#### Optimal
```
<Liam>Yes, that works perfectly. I'll finalize the numbers and send them to you by the end of the day.</Liam>
```

---

### Example 4

#### Context
```
<Chris>I can't decide what to order from this new burger joint. Everything looks delicious.</Chris>
<Pat>I've been here a couple of times, and their special burger is really good.</Pat>
```

#### Query
```
<Chris>Would you recommend trying the special burger, or should I stick with a classic cheeseburger?</Chris>
```

#### Optimal
```
<Pat>I would definitely go with the special burger. It has a unique twist that you won't find in a typical cheeseburger.</Pat>
```

---

### Example 5

#### Context
```
<Jordan>I've been feeling a bit cooped up with all the work lately. Maybe it's time to do something fun over the weekend.</Jordan>
<Taylor>That sounds like a good idea. We haven't done anything adventurous in a while.</Taylor>
```

#### Query
```
<Jordan>How about we try that new escape room in the city?</Jordan>
```

#### Optimal
```
<Taylor>I love that idea! It will be a great challenge and a fun way to spend our weekend.</Taylor>
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
