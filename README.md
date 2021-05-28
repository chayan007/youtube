![alt text](https://i.pinimg.com/originals/08/b1/e6/08b1e6741db060c7d8a0e5a8d4406c56.gif)

### Youtube Search API

Allows users to search API from youtube directly.

#### Setup:

- Clone the repository
- `docker-compose up`

#### Flow:

- Every minute an async task is kicked off to trigger video ingestion process.
- Each page of API response is operated on different tasks.
- Each list of videos (for single page) is then multi-threaded to store into database.
- Four API Keys are used to rotate on basis of quota.

#### Use:

- Hit this API endpoint: `BASE_URL/videos/v1?search=<your search string>` (no authorization)