<template>
  <el-dialog v-model="modal" class="modal-container" style="width: 30%;min-width:400px;height: fit-content;" :show-close="false">
    <template v-slot:header>
      <div class="header-modal">
        Create notification
      </div>
    </template>
    <template v-slot:default>
      <div>
        <el-form>
          <el-row :gutter="20">
            <el-col>
              <el-form-item label="Message" prop="class" label-position="top">
                <el-input v-model="form.message" placeholder="Input message"/>
              </el-form-item>
            </el-col>
            <el-col :span="24" :md="12">
              <el-form-item label="Class" prop="class" label-position="top">
                <el-select v-model="form.class" filterable clearable remote :remote-method="fetchClasses" placeholder="Class">
                  <el-option v-for="item in classList" :key="item.id" :label="item.class_name" :value="item.id"/>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="24" :md="12">
              <el-form-item label="User" prop="user" label-position="top">
                <el-select v-model="form.user" filterable clearable remote :remote-method="fetchUser" placeholder="User">
                  <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id"/>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </template>
    <template v-slot:footer>
      <div>
        <el-button @click="hide">Cancel</el-button>
        <el-button type="primary" @click="send">Confirm</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import {debounce} from "lodash";
import ClassService from "@/service/class-api/api.ts";
import UserService from "@/service/user-api/api.ts";
import NotificationService from "@/service/notification-api/api.ts";

export default {
  name: 'SendNotificationComponent',
  data(){
    return{
      modal: false,
      form: {
        message: "",
        class: null,
        user: null
      },
      classList: [],
      classDebounce: null,
      userDebounce: null,
      loading: {
        class: false,
        user: false
      },
      userList: []
    }
  },
  created() {
    this.fetchClasses()
    this.fetchUser()
  },
  methods:{
    show(){
      this.modal = true
    },

    hide(){
      this.form = {
        message: "",
        class: null,
        user: null
      }
      this.modal = false
    },

    fetchClasses(filter){
      this.classDebounce?.cancel()
      this.classDebounce = debounce(()=>{
            this.loading.class = true
            ClassService.getAllClasses(filter).then((data) =>{
                  this.classList = data.data
                }
            ).catch((error)=>{
              console.log(error)}
            ).finally(()=>{
              this.loading.class = false
            })
          }
          , 1500)()
    },

    fetchUser(filter){
      const query = {
        name: filter
      }
      this.userDebounce?.cancel()
      this.userDebounce = debounce(()=>{
        this.loading.user = true
        UserService.GetUsers(query).then(data =>{
          this.userList = data.data.data
        }).catch(error =>{
          console.log(error)
        }).finally(()=>{
          this.loading.user = false
        })
      },1500)()
    },

    send(){
      NotificationService.CreateNotification(this.form).then(data => {
        console.log(data)
        this.$message(
            {
              message: 'Send notification success',
              type: 'success'
            }
        )
        this.hide()
      }).catch(error =>{
        console.log(error)
        this.$message(
            {
              message: 'Something went wrong',
              type: 'error'
            }
        )
      })
    }
  }
}
</script>