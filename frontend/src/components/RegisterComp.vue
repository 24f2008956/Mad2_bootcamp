<template>
    <div class="container justify-content-center d-flex mt-5">
        <div class="card" style="width:18rem;">
           <div class="card-header">
                Register
            </div>
            <form @submit.prevent="register"> 
            <div class="card-body">
                <div v-if="errorMessage" class="alert alert-primary" role="alert">
                    {{ errorMessage }}
                </div>
                <div class="form-floating mb-3">
                    <input type="email" class="form-control" v-model="formdata.email" id="floatingInput" placeholder="name@example.com">
                    <label for="floatingInput">Email address</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="password" class="form-control" v-model="formdata.password" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" v-model="formdata.name" id="floatingName" placeholder="Name">
                    <label for="floatingName">Name</label>
                </div>
            
                <button class="btn btn-primary mt-3" @click="register">Register</button>
            </div>
            </form>
        </div>

    </div>

</template>
<script>
export default ({
    name: "RegisterComp",
    data() {
        return {
            formdata: {
                email: "",
                password: "",
                name:""
                
            }, 
            errorMessage: "",
        }
    },
    methods:{
        async register(){
            try{
                const response = await fetch("http://127.0.0.1:5000/register",{
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formdata)
                })
                const data = await response.json()
                if(response.status === 200){
                    this.$router.push(`/login`);
                }
                else{
                    this.errorMessage = data.message    
                }

            }
            catch(error){
                console.log("error occured")
            } 
        }
    }

})

</script>