<template>
  <el-header class="header">
    <el-text size="large" class="name" style="font-weight: bold;font-size: 24px">Welcome back {{ user.name }}</el-text>
    <el-dropdown>
      <el-button v-if="user" class="el-dropdown-link">
        <Avatar v-if="user" :name="user.name"/>
        <el-text size="large" class="name" style="font-weight: bold">{{ user.name }}</el-text>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="handleLogOut">Log out</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </el-header>
</template>

<script lang="ts">
import Avatar from "@/components/dashboard/avatar.vue";
export default {
  name: 'navbar',
  components:{
    Avatar
  },
  data(){
    return{
      user: JSON.parse(localStorage.getItem('user'))
    }
  },
  methods:{
    handleLogOut(){
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="css" scoped>
.header {
  background-color: #023e8a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-dropdown-link{
  background-color: #9bb9ff;
  height: 50px;
}

.name{
  color: white;
}

.el-dropdown-link:hover{
  .name{
    color: #0a3077;
  }
}

</style>