<template>
    <div class="container justify-content-center d-flex mt-5">
        <div class="card" style="width:18rem;">
           <div class="card-header">
                Register
            </div> 
            <div class="card-body">
                <div class="form-floating mb-3">
                    <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
                    <label for="floatingInput">Email address</label>
                </div>
                <div class="form-floating">
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>
                <button class="btn btn-primary mt-3">Register</button>
            </div>

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
                password: ""
            }
        }
    }

})
</script>