<template>
  <el-dialog v-model="registerModal" :show-close="false" style="width: 80%;min-width:400px;height: auto;padding-bottom: 50px">
    <el-form :model="form" :rules="rules">
      <el-upload ref="uploadImage" v-model:file-list="fileList" accept=".jpg,.jpeg,.png,.gif" :on-error="error" :on-success="success" :before-upload="beforeUpload" :file-size-limit="1024*1024*5" :on-exceed="onExceed" action="http://localhost:5000/api/user/upload-image" list-type="picture-card" draggable="true" :limit="1">
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
          <el-form-item label="Username" prop="username" label-position="top">
            <el-input v-model="form.username" placeholder="Type your username"/>
          </el-form-item>
        </el-col>
        <el-col :span="24" :md="12">
          <el-form-item label="Password" prop="password" label-position="top">
            <el-input v-model="form.password" placeholder="Type your password"/>
          </el-form-item>
        </el-col>
        <el-col :span="24" :md="12">
          <el-form-item label="Confirm password" prop="confirmPassword" label-position="top">
            <el-input v-model="form.confirmPassword" placeholder="Type your password again"/>
          </el-form-item>
        </el-col>
        <el-col :span="24" :md="12">
          <el-form-item label="Name" prop="name" label-position="top">
            <el-input v-model="form.name" placeholder="Type your name"/>
          </el-form-item>
        </el-col>
        <el-col :span="12" :md="6">
          <el-form-item label="Age" prop="age" label-position="top">
            <el-input v-model="form.age" placeholder="Type your age"/>
          </el-form-item>
        </el-col>
        <el-col :span="12" :md="6">
          <el-form-item label="Gender" prop="gender" label-position="top">
            <el-select v-model="form.gender_id" placeholder="Gender">
              <el-option v-for="item in genderList" :key="item.id" :value="item.id" :label="item.gender"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-dialog v-model="dialogVisible" class="preview">
      <img :src="dialogImageUrl" alt="Preview Image" w-full/>
    </el-dialog>
    <template v-slot:footer>
      <div style="position: absolute;bottom: 20px;right: 20px">
        <el-button @click="registerModal = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="register">
          Register
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import {Delete, Plus, ZoomIn} from "@element-plus/icons-vue"
import type {UploadFile} from 'element-plus'
import UserService from "@/service/user-api/api";

export default {
  name: 'RegisterStudentComponent',
  components: {
    Plus,
    ZoomIn,
    Delete
  },
  data() {
    return {
      registerModal: false,
      rules: {},
      form: {
        username: '',
        password: '',
        confirmPassword: '',
        name: '',
        age: null,
        role: 'student',
        face_image: '',
        gender_id: null,
        class_id: null,
      },
      fileList: [],
      dialogImageUrl: '',
      dialogVisible: false,
      genderList: []
    }
  },
  methods: {
    register(){
      this.loading = false
      UserService.Register(this.form).then(data=>{
        this.$emit('register-success',data.data)
      }).catch((error)=>{
        this.loading = false
        this.$message({message:error.response.message,type:'error'});
      })
    },
    show() {
      this.registerModal = true
    },
    hide() {
      this.registerModal = false
    },
    handlePictureCardPreview(file: UploadFile) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
      console.log(this.fileList)
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
    fetchGenders(){
      UserService.GetGender().then(data =>{
        this.genderList = data.data
      })
    },
    success(data){
      this.form.face_image = data.image
    },
    error(){
      this.$message({message:'Something went wrong please try again',type:'error'});
    }
  },
  created() {
    this.fetchGenders()
    // this.fetchUser("")
  }
}
</script>

<style>
.preview {
  position: fixed;
  width: 50% !important;
  min-width: 400px !important;
  height: auto;

  img {
    width: 100%;
  }
}
</style>