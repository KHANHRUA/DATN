<template>
  <div>
    <navbar/>
    <div v-if="$store.state.myRole === 'admin'">
      <manager-admin :role="$store.state.myRole"/>
    </div>
    <div v-if="$store.state.myRole === 'student'">
      <manager-student :role="$store.state.myRole"/>
    </div>
  </div>
</template>
<script lang="ts">
import Navbar from "@/components/dashboard/navbar.vue";
import ManagerAdmin from "@/components/dashboard/manager-admin.vue";
import ManagerStudent from "@/components/dashboard/manager-student.vue";
import UserService from "@/service/user-api/api";
import {ROLES} from "@/utils/constant";

export default {
  name: 'dashboard',
  computed: {
    ROLES() {
      return ROLES
    }
  },
  components: { Navbar, ManagerAdmin, ManagerStudent },
  data(){
  },
  methods:{

  },
  async created() {
    try {
      if(!localStorage.getItem('token')){
        throw Error('no token')
      }
      const data = await UserService.Auth()
      this.$store.commit('setRole', data.data.role);
    }
    catch(error) {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      this.$message({
        message: 'Token hết hạn vui lòng đăng nhập lại',
        type:'error'
      })
      this.$router.push('/login')
    }
  }
}
</script>