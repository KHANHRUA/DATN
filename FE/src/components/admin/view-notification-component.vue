<template>
  <el-dialog v-model="rolesModal" style="width: 70%;min-width:400px;height: fit-content;" :show-close="false">
    <el-row :gutter="20" v-if="role === 'admin'">
      <el-col :xl="3" :md="4">
        <span>Class: </span>
        <el-select v-model="query.class_id" clearable placeholder="Class" @change="pickClass">
          <el-option v-for="item in classList" :key="item.id" :label="item.class_name" :value="item.id"/>
        </el-select>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-table v-loading="loading.table" :data="notificationList" fit>
          <el-table-column
              label="No.0"
              width="100"
          >
            <template v-slot:default="scope">
              <div>
                {{ scope.$index + 1 + (query.page - 1) * query.perPage}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Message"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.message }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Time"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.created_at }}
              </div>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="total > 0" class="demo-pagination-block pagination">
          <el-pagination
              v-model:current-page="query.page"
              v-model:page-size="query.perPage"
              :page-sizes="[10, 20, 50, 100]"
              size="default"
              layout="sizes, prev, pager, next"
              :total="total"
              @size-change="sizeChange"
              @current-change="pageChange"
          />
        </div>
      </el-col>
    </el-row>
    <div>
      <global-modal ref="confirmModal" :width="20" type="danger" @submit="deleteUser">
        <template v-slot:default>
          <div style="font-size: 20px">
            Are you sure ?
          </div>
        </template>
      </global-modal>
    </div>
  </el-dialog>
</template>

<script lang="ts">
import { FilterUser } from '@/interface/user';
import {Edit, Delete, ZoomIn, Plus} from "@element-plus/icons-vue"
import { ROLES } from "@/utils/constant";
import UserService from "@/service/user-api/api";
import GlobalModal from "@/components/common/global-modal.vue";
import ClassService from "@/service/class-api/api";
import {debounce} from "lodash";
import NotificationService from "@/service/notification-api/api";

export default {
  name: 'ViewNotificationComponent',
  data() {
    return{
      rolesModal: false,
      roles:[],
      loading: {
        roles: false,
        class: false,
        table: false
      },
      notificationList: [],
      query: {
        name: '',
        class_id: null,
        page: 1,
        perPage: 20,
      },
      total: 20,
      form: {
        name: '',
        age: null,
        role: 'student',
        face_image: '',
        class_id: null,
        fileList: [],
      },
      rules: {},
      classList: [],
      classDebounce: null,
      dialogVisible: false,
      dialogImageUrl: "",
      userDeleteId: null
    }
  },
  props: {
    role: {
      type: String,
      enum: ['admin','teacher','student'],
      default: 'student'
    }
  },
  components:{
    Plus, ZoomIn,
    GlobalModal,
    Edit, Delete
  },
  created() {
    this.fetchClasses()
    this.fetchNotification()
  },
  methods:{
    show(){
      //reset data
      this.query = {
        name: '',
        class_id: null,
        page: 1,
        perPage: 20,
      }
      this.rolesModal = true
    },

    fetchNotification(filter){
      this.loading.table = true
      NotificationService.getNotification(filter).then(data =>{
        this.notificationList = data.data
      }).catch((error)=>{
        console.log(error)
      }).finally(()=>{
        this.loading.table = false
      })
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

    fetchUser(filter: FilterUser){
      this.loading.table = true
      UserService.GetUsers(filter).then(data =>{
        this.userList = data.data.data
      }).catch(error =>{
        console.log(error)
      }).finally(()=>{
        this.loading.table = false
      })
    },

    sizeChange(size: number){
      this.query.perPage = size
      this.fetchUser(this.query)
    },

    pageChange(page :number){
      this.query.page = page
      this.fetchUser(this.query)
    },

    openConfirmModal(data){
      this.userDeleteId = data.id
      this.$refs.confirmModal.show()
    },

    pickClass(){
      this.fetchNotification(this.query)
    },

    deleteUser(){
      this.loading.table = true
      UserService.DeleteUser(this.userDeleteId).then((data)=>{
        this.fetchUser(this.query)
        this.$refs.confirmModal.hide()
        this.$message(
            {
              message: 'Delete user successful!',
              type: 'success'
            }
        )
      }).catch((error)=>{
        console.log(error)
        this.$message(
            {
              message: 'Something went wrong',
              type: 'error'
            }
        )
      }).finally(()=>{
        this.loading.table = false
      })
    }
  }
}
</script>

<style scoped>

</style>