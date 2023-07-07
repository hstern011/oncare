# How to run this project
1. Clone the git repository
2. Install dependencies using pip:
```
pip install -r requirements.txt
```
3. Change to the `/myapi/ directory` (`cd myapi`) and run migrations to set up the database:
```
python manage.py migrate
```
4. Start the Django server by running:
```
python manage.py runserver
```
5. API can then be accessed at http://127.0.0.1:8000/

# How it works
The API provides details on Visits and Revisions. A Revision is a state of the schedule, and a Visit is a single element in the schedule. Whenever a change is made to the schedule - i.e. a Visit is added, updated, or removed - a Revision to the schedule is made. However, all past Revisions are still available through the API.
When a Visit is created, it is assigned a `public_id` that can be used in future API calls to update it.

# My approach to the problem
Whilst this was very much a 'learn as I go' task for me due to my limited experience with Django, it was a good opportunity to direct my learning!

I initially had to consider the best practice and approach for how to ensure the persistence of data across revisions - I originally considered duplicating every Visit object with every new Revision, to ensure all Visit records were distinct across revisions. However, I felt that this solution was not very scaleable, so instead opted to implement a many-many relationship between Revisions and Visits - i.e. if a real-world visit exists in multiple Revisions, this is referring to a single Visit record in the database.

This also necessitated including an extra non-unique 'public_id' field for Visits, to give users the 'appearance' of editing a single record when they make changes, when in fact a distinctly new record is created with each change. This was done using UUIDs - so uniqueness is guaranteed when required, but then can also be re-used in new records.

In general, the code works such that when a Visit is added/updated/deleted, the API creates a duplicate of the most recent Revision (and for POST/PUT requests, a new Visit record), with relational links to all Visits of the previous Revision, minus the Visit that is being updated or deleted (in the case of PUT/DELETE), or plus the Visit that is being created (in the case of POST).


# Endpoints available:
## `GET: /schedule/latest`
Returns the most recent Revision, i.e. the current state of the schedule. This is returned as a single JSON Revision object, with a field `visit_set` that contains a list of all Visit objects in the schedule.

## `GET: /schedule/revision{id}`
Returns the contents of any Revision given the ID.
E.g. /schedule/revision4

## `GET: /schedule/all`
Returns a complete list of all past Revisions.

## `POST: /schedule/`
Adds a new visit to the schedule. Payload required fields are `start_date_time`, `end_date_time`, `client`, and `carer`. Example :
```
{
    "start_date_time": "2023-06-26T23:00:00.000Z",
    "end_date_time": "2023-06-27T22:59:59.999Z",
    "client": 1,
    "carer": 1
}
```

## `PUT /schedule/visit/{public_id}`
Updates the details of the visit specified by the `public_id`. Payload must be in the same format as above.

## `DELETE /schedule/visit/{public_id}`
Deletes the visit specified by the `public_id` from the schedule.


# Admin UI
There is also a basic admin UI for viewing the data stored. Go to the endpoint `/schedule/admin`, and login in with the username `admin` and password `1234`. This will allow you to explore all Revisions and Visits in the system interactively. It has been set up to make all data read-only, even from this interface.


# Next steps/limitations
Given more time, I would have liked to explore further how to impose restrictions on the data at the database-level, in order to further protect the data from accidental mutations within the code.