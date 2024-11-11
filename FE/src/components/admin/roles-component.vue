<template>
  <el-dialog v-model="rolesModal" style="width: 70%;min-width:400px;height: fit-content;" :show-close="false">
    <el-row :gutter="20">
      <el-col :xl="6" :md="8">
        <span>Name: </span>
        <el-input v-model="query.name" placeholder="name"/>
      </el-col>
      <el-col :xl="3" :md="4">
        <span>Roles: </span>
        <el-select v-model="query.role" clearable placeholder="Role">
          <el-option v-for="item in roles" :key="item" :label="item" :value="item"/>
        </el-select>
      </el-col>
      <el-col :xl="3">
        <br/>
        <el-button type="primary" @click="searching">
          Search
        </el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-table v-loading="loading.table" :data="userList" fit>
          <el-table-column
            label="No.0"
          >
            <template v-slot:default="scope">
              <div>
                {{ scope.$index + 1 + (query.page - 1) * query.perPage}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Name"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Age"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.age }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Image"
          >
            <template v-slot:default="{row}">
              <div v-if="row.face_image">
                <el-image :src="row.face_image" alt="avatar" lazy style="width: 20%;min-width: 50px"/>
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Gender"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.gender_id }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Class"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.class_id }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Role"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.role }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Action"
          >
            <template v-slot:default="{row}">
              <div style="display:flex;min-width: fit-content">
                <el-icon class="icon-action icon-primary" style="margin-right: 15px" @click="openModalEdit(row)"><Edit/></el-icon>
                <el-icon class="icon-action icon-danger" @click="openConfirmModal(row)"><Delete/></el-icon>
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
      <global-modal ref="editModal">
        <template v-slot:header>
          <div class="header-modal">
            Edit information
          </div>
        </template>
        <template v-slot:default>
          <el-form :model="form" :rules="rules">
            <el-upload ref="uploadImage" v-model:file-list="form.fileList" accept=".jpg,.jpeg,.png,.gif" :on-error="error" :on-success="success" :before-upload="beforeUpload" :file-size-limit="1024*1024*5" :on-exceed="onExceed" action="http://localhost:5000/api/user/upload-image" list-type="picture-card" draggable="true" :limit="1">
              <el-icon>
                <Plus/>
              </el-icon>
              <template #file="{ file }">
                <div>
                  <img :src="file.url" alt="" class="el-upload-list__item-thumbnail"/>
                  <span class="el-upload-list__item-actions">
              <span
                  class="el-upload-list__item-preview"
                  @click="handlePictureCardPreview(file)"
              >
                <el-icon>
                  <zoom-in/>
                </el-icon>
              </span>
              <span
                  class="el-upload-list__item-delete"
                  @click="handleRemove(file)"
              >
                <el-icon>
                  <Delete/>
                </el-icon>
              </span>
            </span>
                </div>
              </template>
            </el-upload>
            <br/>
            <el-row :gutter="20">
              <el-col :span="24" :md="12">
                <el-form-item label="Name" prop="name" label-position="top">
                  <el-input v-model="form.name" placeholder="Type your name"/>
                </el-form-item>
              </el-col>
              <el-col :span="24" :md="6">
                <el-form-item label="Class" prop="class" label-position="top">
                  <el-select v-model="form.class_id" filterable remote :remote-method="fetchClasses" placeholder="Class">
                    <el-option v-for="item in classList" :key="item.id" :label="item.class_name" :value="item.id"/>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="24" :md="6">
                <el-form-item label="Role" prop="role" label-position="top">
                  <el-select v-model="form.role" clearable placeholder="Role">
                    <el-option v-for="item in roles" :key="item" :label="item" :value="item"/>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12" :md="6">
                <el-form-item label="Age" prop="age" label-position="top">
                  <el-input v-model="form.age" placeholder="Type your age"/>
                </el-form-item>
              </el-col>
              <el-col :span="12" :md="6">
                <el-form-item label="Age" prop="age" label-position="top">
                  <el-input v-model="form.age" placeholder="Type your age"/>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-dialog v-model="dialogVisible" class="preview">
            <img :src="dialogImageUrl" alt="Preview Image" w-full/>
          </el-dialog>
        </template>
      </global-modal>
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
import { FilterUser, User } from '@/interface/user';
import {Edit, Delete, ZoomIn, Plus} from "@element-plus/icons-vue"
import { ROLES } from "@/utils/constant";
import UserService from "@/service/user-api/api";
import GlobalModal from "@/components/common/global-modal.vue";
import type {UploadFile} from "element-plus";
import ClassService from "@/service/class-api/api";
import {debounce} from "lodash";

export default {
  name: 'RolesComponent',
  data() {
    return{
      rolesModal: false,
      roles:[],
      loading: {
        roles: false,
        class: false,
        table: false
      },
      userList: [],
      query: {
        name: '',
        role: ROLES.STUDENT,
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
  components:{
    Plus, ZoomIn,
    GlobalModal,
    Edit, Delete
  },
  created() {
    this.fetchUser(this.query)
    this.fetchRoles()
    this.fetchClasses()
  },
  methods:{
    show(){
      //reset data
      this.query = {
        name: '',
        role: ROLES.STUDENT,
        page: 1,
        perPage: 20,
      },
      this.fetchUser(this.query)
      this.rolesModal = true
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

    fetchRoles(){
      this.loading.roles = true
      UserService.GetRoles().then((data) =>{
          this.roles = data.data
        }
      ).catch((error)=>{
        console.log(error)}
      ).finally(()=>{
        this.loading.roles = false
      })
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

    searching(){
      this.fetchUser(this.query)
    },

    openModalEdit(data: User){
      this.form = {
        name: data.name,
        age: data.age,
        role: data.role,
        face_image: data.face_image,
        class_id: data.class_id,
        fileList: [{
          name: 'current.png',
          url: data.face_image
        }]
      }
      this.$refs.editModal.show()
    },

    handlePictureCardPreview(file: UploadFile) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },

    handleRemove(){
      this.$refs.uploadImage.clearFiles()
    },

    onExceed(){
      this.$message({
        message: 'Max upload one image',
        type: 'error'
      })
    },

    beforeUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isPNG = file.type === 'image/png';
      const isGIF = file.type === 'image/gif';
      const isLt5M = file.size / 1024 / 1024 < 5;

      if (!isJPG && !isPNG && !isGIF) {
        this.$message({message:'Only jpg, png, gif files are allowed!',type:'warning'});
        return false;
      }
      if (!isLt5M) {
        this.$message({message:'File size cannot exceed 5MB!',type:'warning'});
        return false;
      }
      return true;
    },

    success(data: object){
      this.form.face_image = data.image
    },

    error(){
      this.$message({message:'Something went wrong please try again',type:'error'});
    },

    openConfirmModal(data){
      this.userDeleteId = data.id
      this.$refs.confirmModal.show()
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