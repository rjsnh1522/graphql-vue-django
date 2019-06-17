<template>
  <div class="hello">
    <h5>Getting data from graphql</h5>
    <!-- first way of querying -->
    <!-- <div v-for="rec in recipes" :key="rec.id">
          {{rec.title}} {{rec.description}}
    </div> -->

    <ApolloQuery :query="require('../graphql/allAssets.gql')">
      <template v-slot="{result: {loading, error, data}}"> 
          <div v-if="data">
            <div v-for="rec in data.assets" :key="rec.id">{{rec.handle}} <span> {{rec.fileName}}</span></div> 
          </div>
      </template>
    </ApolloQuery>

    <!-- mutation -->
    <!-- <ApolloMutation :mutation="require('../graphql/addAssets.gql')"
                    :variable="{title, password}"
                    @done="onDone">
      <template v-slot="{mutate}">
        <form v-on:submit.prevent="mutate()">
            <label for="title"> Email</label>
            <input v-model="title">
        </form>
        
      </template>
      

    </ApolloMutation> -->


  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  apollo: {
    assets: gql`
      query allAssets{
        assets{
            id
            handle
            fileName
            size
        }
      }`
  },
  methods: {
    onDone(){
      console.log('One done')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
