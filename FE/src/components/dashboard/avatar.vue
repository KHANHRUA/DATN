<template>
  <div class="avatar" :style="{backgroundColor: getColor()}">
    {{text}}
  </div>
</template>

<script lang="ts">
export default {
  name: 'avatar',
  props:{
    name:{
      type: String,
      default: ''
    }
  },
  data(){
    return{
      text: ''
    }
  },
  methods:{
    getColor(){
      this.text = this.name[0].toUpperCase()
      switch (this.text) {
        case 'A':
        case 'E':
        case 'I':
        case 'O':
        case 'U':
          return 'red'; // Adjust colors as needed
        default:
          return 'blue';
      }
    }
  }
}
</script>

<style lang="css" scoped>
.avatar{
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: black;
  margin-right: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}
</style>