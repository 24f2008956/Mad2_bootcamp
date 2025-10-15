<template>
    
    <div class="container justify-content-center d-flex mt-5">

        <div class="card" style="width:18rem;">
            <div class="card-header">
                Login
            </div>
            <div class="card-body">
                <div v-if="errorMessage" class="alert alert-primary" role="alert">
                    {{ errorMessage }}
                </div>
                <div class="form-floating mb-3">
                    <input type="email" v-model="formdata.email" class="form-control" id="floatingInput"
                        placeholder="name@example.com">
                    <label for="floatingInput">Email address</label>
                </div>
                <div class="form-floating">
                    <input type="password" v-model="formdata.password" class="form-control" id="floatingPassword"
                        placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>
                <button class="btn btn-primary mt-3" @click="login">Login</button>
            </div>

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
            },
            errorMessage: "",
        }
    },
    methods: {
        async login() {
            console.log("login clicked");
            console.log(this.formdata)
            try {
                const response = await fetch("http://127.0.0.1:5000/login", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formdata)
                })
                console.log("fullfilled")
                const data = await response.json()
                if (response.status === 200) {
                    localStorage.setItem("token", data.token);
                    if (data.role==="user")
                        this.$router.push(`/user/dashboard`);
                    else if (data.role === "admin"){
                        this.$router.push(`/admin/dashboard`);
                    }
                }
                else {
                    this.errorMessage = data.message
                }
            }
            catch (error) {
                console.log("rejected")
                console.log("error occured", error.message);
            }
        }


    }
}

)

</script>