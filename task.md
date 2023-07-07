# Scenario

As a care agency office staff I need to see a list of schedule visits. Schedule visits explain which care worker will be visiting which client at which time. I need a method to create, update and delete schedule visits in an immutable way so as to be compliant with various regulations.

# Your Task

Produce the code required to power an API where the user can request mutations but the underlying data is preserved for introspection and retrieval.
Take illustrated payloads and URLs as being a guide not a hard requirement.

## Deliverables

* A git repository with your code.
* A README.md file with instructions on how to run your code.
* A short description of your approach to the problem.


## Flow of requests and responses

Given I `GET`: `/schedule/latest`, I receive the response:

```json
[]
```

---

Given I then `POST`: `/schedule/`
With the payload:

```json
{
    "start_date_time": "2023-06-26T23:00:00.000Z",
    "end_date_time": "2023-06-27T22:59:59.999Z",
    "client": 1,
    "carer": 1
}
```

Then given I `GET`: `/schedule/latest` or `/schedule/:revision1`, I receive the response:
Note param `revision1` can be whatever you choose to represent fetching a state in time
Note the `id` can be in whatever form you choose (primary int, UUID...)

```json
[
    {
        "id": "ABC-123",
        "start_date_time": "2023-06-26T23:00:00.000Z",
        "end_date_time": "2023-06-27T22:59:59.999Z",
        "client": 1,
        "carer": 1
    }
]
```

---

Given I then `PUT`: `/schedule/visit/ABC-123`
With the payload:

```json
{
    "start_date_time": "2023-06-26T23:00:00.000Z",
    "end_date_time": "2023-06-27T21:59:59.999Z", # Notice the changed time
    "client": 1,
    "carer": 2 # Notice the changed carer
}
```

Then given I `GET`: `/schedule/latest` or `/schedule/:revision2`, I receive the response:

```json
[
    {
        "id": "ABC-123",
        "start_date_time": "2023-06-26T23:00:00.000Z",
        "end_date_time": "2023-06-27T21:59:59.999Z",
        "client": 1,
        "carer": 2
    }
]
```

And given I `GET`: `/schedule/:revision1`, I receive the original response:

```json
[
    {
        "id": "ABC-123",
        "start_date_time": "2023-06-26T23:00:00.000Z",
        "end_date_time": "2023-06-20T23:59:00",
        "client": 1,
        "carer": 1
    }
]
```

---

Given I then `DELETE`: `/schedule/visit/ABC-123`

Then given I `GET`: `/schedule/latest` or `/schedule/:revision3`, I receive the response:

```json
[]
```

And given I `GET`: `/schedule/:revision2`, I receive the previous response:

```json
[
    {
        "id": "ABC-123",
        "start_date_time": "2023-06-26T23:00:00.000Z",
        "end_date_time": "2023-06-27T21:59:59.999Z",
        "client": 1,
        "carer": 2
    }
]
```

Bonus features if you have time:

* Ability to filter by a date range
* A UI to see visits
