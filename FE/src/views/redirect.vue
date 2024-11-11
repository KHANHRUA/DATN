<template>
  <div>

  </div>
</template>
<script lang="ts">
export default {
  name: 'redirect',
  mounted() {
    this.redirect()
  },
  methods:{
    redirect(){
      this.$router.push('/login');
    }
  }
}
</script>