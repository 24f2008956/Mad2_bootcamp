<template>
    <div class="text-center">
        <h2>Welcome to Smart Vehivle Parking</h2>
        <div class="">
            <router-link to="/login" class="btn btn-primary me-2">Login</router-link>
            <button  @click="gotoregister" class="btn btn-primary">Register</button>
        </div>
    </div>

</template>
<script>
export default ({
    name: "LoginComp",
    data() {
        return {
            formdata: {
                email: "",
                password: ""
            }
        }
    },
    methods:{
        gotoregister(){
            this.$router.push("/register");
        }
    }

})

</script>