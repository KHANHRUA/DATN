<template>
  <el-container class="dashboard">
    <el-row class="rowDashBoard">
      <el-col :span="24" :md="10">
        <el-row class="containOption" :gutter="20">
          <el-col :span="24" style="padding: 20px">
            <el-text class="title">
              {{'Manager'}}
            </el-text>
          </el-col>
          <el-col :span="12">
            <el-button class="buttonManager" @click="openRolesModal()">
              <el-icon class="icon">
                <User />
              </el-icon>
              <el-text class="feature">
                {{'User'}}
              </el-text>
            </el-button>
            <roles-component ref="roles"/>
          </el-col>
          <el-col :span="12">
            <el-button class="buttonManager">
              <el-icon class="icon">
                <Finished />
              </el-icon>
              <el-text class="feature">
                {{'Attendance'}}
              </el-text>
            </el-button>
          </el-col>
          <el-col :span="12">
            <el-button class="buttonManager" @click="openSendNotificationModal">
              <el-icon class="icon">
                <Promotion />
              </el-icon>
              <el-text class="feature">
                {{'Send notification'}}
              </el-text>
            </el-button>
            <SendNotificationComponent ref="sendNotification"/>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="24" :md="10">
        <el-row class="containOption" :gutter="20">
          <el-col :span="24" style="padding: 20px">
            <el-text class="title">
              {{'Setting'}}
            </el-text>
          </el-col>
          <el-col :span="12">
            <el-button class="buttonManager" @click="openScheduleEdit">
              <el-icon class="icon">
                <Clock />
              </el-icon>
              <el-text class="feature">
                {{'Schedule'}}
              </el-text>
            </el-button>
            <schedule-edit-component ref="scheduleEdit"/>
          </el-col>
          <el-col :span="12">
            <el-button class="buttonManager" @click="openViewNotificationModal">
              <el-icon class="icon">
                <BellFilled />
              </el-icon>
              <el-text class="feature">
                {{'Notification'}}
              </el-text>
            </el-button>
            <ViewNotificationComponent ref="viewNotification" :role="role"/>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </el-container>
</template>
<script lang="ts">
import RolesComponent from "@/components/admin/roles-component.vue";
import {User, Switch, Finished, Clock, BellFilled, Promotion} from "@element-plus/icons-vue"
import SendNotificationComponent from "@/components/admin/send-notification-component.vue";
import ViewNotificationComponent from "@/components/admin/view-notification-component.vue";
import ScheduleEditComponent from "@/components/admin/schedule-edit-component.vue";

export default {
  name: 'adminDashboard',
  components:{
    ScheduleEditComponent,
    SendNotificationComponent,
    ViewNotificationComponent,
    RolesComponent,
    User,
    Switch,
    Finished,
    Clock,
    BellFilled,
    Promotion
  },
  props: {
    role: {
      type: String,
      enum: ['admin','teacher','student'],
      default: 'student'
    }
  },
  data(){
    return{
      rolesModal: false
    }
  },
  methods:{
    openRolesModal(){
      this.$refs.roles.show()
    },
    openSendNotificationModal(){
      this.$refs.sendNotification.show()
    },
    openViewNotificationModal(){
      this.$refs.viewNotification.show()
    },
    openScheduleEdit(){
      this.$refs.scheduleEdit.show()
    }
  }
}
</script>
<style lang="css">
.el-col-24{
  margin-bottom: 10px;
}

.buttonManager{
  width: 100%;
  padding-top: 100% !important;
  border-radius: 20px !important;
  margin-top: 10px;
  background-color: #f4f5f7 !important;
  position: relative;
}

.dashboard{
  display: flex;
  justify-content: center;
  padding: 30px;
  min-height: 100vh;
  background-color:  #c1d8ff;
  overflow-x: hidden;
  .rowDashBoard{
    display: flex;
    justify-content: space-between;
    min-width: 380px;
    width: 70%;
  }
  .containOption{
    border-radius: 10px;
    box-shadow: -2px 2px 15px rgba(173, 193, 199, 0.62);
    background-color: #dbecff;
    padding-bottom: 15px;
  }
  .title{
    font-size: 30px;
    color: #0a3077;
    font-weight: 900;
  }
  .feature{
    position: absolute;
    bottom: 5px;
    font-size: 20px;
    left: 50%;
    color: #24466b;
    transform: translateX(-50%);
    font-weight: 700;
  }
  .icon{
    width: 100px;
    height: 100px;
    background-color: #9bb9ff;
    font-size: 50px;
    position: absolute;
    border-radius: 25px;
    color: #f4f5f7;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);;
  }
}
</style>