# VoteSecure API Documentation

## Base URL
```
http://localhost:8002/api/
```

## Authentication
Most endpoints use Session Authentication. Users must be logged in through Django's session system.

## Endpoints

### Positions

#### List All Positions
```
GET /api/positions/
```
Returns all positions with their associated candidates.

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "President",
    "description": "Lead the organization and represent students",
    "max_votes_allowed": 1,
    "candidates": [
      {
        "id": 1,
        "name": "Sarah Johnson",
        "party": "Progressive Alliance",
        "bio": "Experienced leader with 5 years in student government.",
        "position": 1
      }
    ]
  }
]
```

#### Get Position Detail
```
GET /api/positions/{id}/
```
Returns details of a specific position with candidates.

### Candidates

#### List All Candidates
```
GET /api/candidates/
```
Returns all candidates across all positions.

#### Get Candidate Detail
```
GET /api/candidates/{id}/
```
Returns details of a specific candidate.

### Voting

#### Check Voting Status
```
GET /api/user/status/
```
**Authentication Required**

Returns whether the current user has voted.

**Response Example:**
```json
{
  "has_voted": false,
  "username": "john_doe"
}
```

#### Submit Votes
```
POST /api/vote/submit/
```
**Authentication Required**

Submit votes for all positions at once.

**Request Body:**
```json
{
  "votes": [
    {
      "position_id": 1,
      "candidate_id": 2
    },
    {
      "position_id": 2,
      "candidate_id": 5
    }
  ]
}
```

**Response Example:**
```json
{
  "status": "success",
  "message": "Your votes have been submitted successfully",
  "votes_count": 4
}
```

#### List My Votes
```
GET /api/votes/
```
**Authentication Required**

Returns all votes cast by the current user.

### User

#### Get User Profile
```
GET /api/user/profile/
```
**Authentication Required**

Returns the current user's profile information.

**Response Example:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "has_voted": true
}
```

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Error description"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Testing the API

### Using curl

**Get all positions:**
```bash
curl http://localhost:8002/api/positions/
```

**Submit votes (requires authentication):**
```bash
curl -X POST http://localhost:8002/api/vote/submit/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "votes": [
      {"position_id": 1, "candidate_id": 1},
      {"position_id": 2, "candidate_id": 4}
    ]
  }'
```

### Using Django REST Framework Browsable API

Navigate to any endpoint in your browser while logged in to use the interactive API interface:
```
http://localhost:8002/api/positions/
```
