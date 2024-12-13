<template>
  <div>
    <navbar/>
    <div v-if="$store.state.myRole === 'admin'">
      <manager-admin :role="$store.state.myRole"/>
    </div>
    <div v-if="$store.state.myRole === 'teacher'">
      <manager-teacher :role="$store.state.myRole"/>
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
import ManagerTeacher from "@/components/dashboard/manager-teacher.vue";
import UserService from "@/service/user-api/api";
import {ROLES} from "@/utils/constant";
import {socket} from "@/service/socket.service";
import {changeTimestampToTime} from "@/utils/function";

export default {
  name: 'dashboard',
  computed: {
    ROLES() {
      return ROLES
    }
  },
  components: { Navbar, ManagerAdmin, ManagerStudent, ManagerTeacher },
  data(){
  },
  methods:{
    async Notice(data){
      Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
          console.log(data.data)
          const {room, session,typeCheck,user} = data.data
          if(user.id === JSON.parse(localStorage.getItem('user')).id){
            new Notification('You have check successful', {
              body: `You have check ${typeCheck? 'in' : 'out'} room ${room.room_name}, the session is start at ${this.getDayOfWeek(session.start_at)}, ${changeTimestampToTime(session.start_at/1000)}`
            })
          }
        } else {
          console.log("cấp quyền không thành công");
        }
      })
    },

    getDayOfWeek(timestamp) {
      const daysOfWeek = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];
      const date = new Date(timestamp);
      return daysOfWeek[date.getDay()];
    },
  },
  async created() {
    try {
      if(!localStorage.getItem('token')){
        throw Error('no token')
      }
      await Notification.requestPermission()
      const data = await UserService.Auth()
      this.$store.commit('setRole', data.data.role);
      const dataSocket = {
        class_id: data.data.class_id
      }
      socket.emit('login', dataSocket)
      socket.on('attendant', (data) => {
        this.Notice(data)
      })
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