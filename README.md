# graphql-vue-django

Python django and vue app for using graphql

ToDo

Add Mongodb

Add ElasticSearch

Implement django-channels

```
{
  tracks {
    id
    title
    description
  }
}


mutation {
  tokenAuth(username:"Reed", password:"123456789"){
    token
    
  }
}

{
  user(id:1){
    id
    password
    username
    email
  }
}



mutation {
  createUser(username: "Reed", password:"123456789",
  email:"reed@yahoo.com"){
    user{
      id
      password
      email
      username
    }
    
  }
}


mutation {
  createTrack(title: "Track 5", 
    description: "Track 5 Description",
    url:"https://track5.com"){
    track{
      id
      title
      description
      url
      createdAt
    }
  }
}

mutation {
  updateTrack(trackId:5,
  title:"Updated track 5",
  description:"updated description",
  url:"https://updatedtrack5.com"){
    track{
      id
      title
    }
  }
}

query{
  tracks{
    id
    title
    description
    postedBy{
      id
    }
  }
}

mutation {
  tokenAuth(username:"Reed", password:"123456789"){
    token
    
  }
}

mutation {
  deleteTrack(trackId:5){
    trackId
  }
}

query {
  likes{
    id
    user{
      id
      username
    }
    track{
      id
      url
    }
  }
}

mutation {
  deleteTrack(trackId:5){
    trackId
  }
}


```
