<template>
  <div class="container">
    <div class="top"></div>
    <div class="bottom"></div>
    <div class="center">
      <h2>Please Sign In</h2>
      <el-form ref="loginForm" :model="form" :rules="rules">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Username">
            <template v-slot:suffix>
              <el-icon>
                <UserFilled/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" :type="passwordType" placeholder="Password">
            <template v-slot:suffix>
              <div style="display: flex;justify-content: center;align-items: center" @click="changePasswordType">
                <el-icon v-if="passwordType === 'password'">
                  <Hide  style="cursor: pointer"/>
                </el-icon>
                <el-icon v-else>
                  <View style="cursor: pointer"/>
                </el-icon>
              </div>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="handleLogin">Login</el-button>
      <el-text class="register" @click="openRegisterModal">
        Register
      </el-text>
    </div>
    <Register ref="register" @register-success="registerSuccess"/>
    <div v-if="loading" class="loadingContainer">
      <span class="loader"></span>
    </div>
  </div>
</template>
<script lang="ts">
import UserService from "@/service/user-api/api";
import loading from "@/mixin/loading.vue";
import Register from "@/components/student/register.vue";
import {Hide, View, UserFilled} from "@element-plus/icons-vue"

export default {
  name: 'login',
  mixins: [loading],
  components:{
    Register,
    Hide,View, UserFilled
  },
  data(){
    return{
      form: {
        username: '',
        password: ''
      },
      rules:{
        username: [{required: true, message: 'Username is required'}],
        password: [{required: true, message: 'Password is required'}],
      },
      passwordType: 'password',
    }
  },
  methods:{
    changePasswordType(){
      this.passwordType = this.passwordType === 'password'? 'text': 'password'
    },

    openRegisterModal(){
      this.$refs.register.show()
    },

    registerSuccess(data){
      this.form = data
      this.handleLogin()
    },

    handleLogin(){
      this.loading = true
      UserService.Login(this.form).then(data =>{
        this.loading = false
        localStorage.setItem('token', data.data.access_token)
        localStorage.setItem('user', JSON.stringify(data.data.user))
        this.$message(
            {
              message: 'Đăng nhập thành công',
              type: 'success'
            }
        )
        this.$router.push('/dashboard');
      }).catch(error =>{
        this.loading = false
        this.$message(
            {
              message: error.response && error.response.data && error.response && error.response.data.error,
              type: 'error'
            }
        )
      })
    }
  }
}
</script>

<style scoped>
*, *:before, *:after {
  box-sizing: border-box
}

body {
  min-height: 100vh;
}

.register{
  text-decoration: underline;
  cursor: pointer;
  color: #0a3077;
}

.container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;

  &:hover, &:active {
    .top, .bottom {
      &:before, &:after {
        margin-left: 200px;
        transform-origin: -200px 50%;
        transition-delay: 0s;
      }
    }

    .center {
      opacity: 1;
      transition-delay: 0.2s;
    }
  }
}

.top, .bottom {
  &:before, &:after {
    content: '';
    display: block;
    position: absolute;
    width: 200vmax;
    height: 200vmax;
    top: 50%;
    left: 50%;
    margin-top: -100vmax;
    transform-origin: 0 50%;
    transition: all 0.5s cubic-bezier(0.445, 0.05, 0, 1);
    z-index: 10;
    opacity: 0.65;
    transition-delay: 0.2s;
  }
}

.top {
  &:before {
    transform: rotate(45deg);
    background: #e46569;
  }

  &:after {
    transform: rotate(135deg);
    background: #ecaf81;
  }
}

.bottom {
  &:before {
    transform: rotate(-45deg);
    background: #60b8d4;
  }

  &:after {
    transform: rotate(-135deg);
    background: #3745b5;
  }
}

.center {
  position: absolute;
  width: 400px;
  height: 400px;
  top: 50%;
  left: 50%;
  margin-left: -200px;
  margin-top: -200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px;
  opacity: 0;
  transition: all 0.5s cubic-bezier(0.445, 0.05, 0, 1);
  transition-delay: 0s;
  color: #333;

  input {
    width: 100%;
    padding: 15px;
    margin: 5px;
    border-radius: 1px;
    border: 1px solid #ccc;
    font-family: inherit;
  }
}
</style>