//psycopg2-binary==2.9.1
//return primise with Auth token by passing username and password in body

var tok = ""

var a = fetch('https://whispering-peak-32557.herokuapp.com/api-token-auth/', { 
   method: 'post', 
   headers: new Headers({
     'Content-Type': 'application/x-www-form-urlencoded'
   }), 
   body: 'username=admin&password=root'
 }).then(function(res) {
    return res.json();
   })


 a.then((token) => tok = token.token)

 localStorage.setItem('token' , tok)
  
  

  





//return object  access only by token
obj = ""
var promise = fetch('https://whispering-peak-32557.herokuapp.com/objects/1/', { 
   method: 'get', 
   headers: new Headers({
     'Accept': 'application/json',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Authorization': 'Token ' + localStorage.token,
   }), 

 }).then(function(res) {
    return res.json();
   })
  .then(function(resJson) {
    return resJson;
   })

  promise.then((response)=> obj = response)



//return list of objects
var obs = ""

var objs = fetch('https://whispering-peak-32557.herokuapp.com/objects/', { 
   method: 'get', 
   headers: new Headers({
     'Accept': 'application/json',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Authorization': 'Token ' + localStorage.token,
   }), 

 }).then(function(res) {
    return res.json();
   })
  .then(function(resJson) {
    return resJson;
   }).then((objects) => obs = objects)


  //post new object

  fetch('https://whispering-peak-32557.herokuapp.com/objects/', { 
   method: 'post', 
   headers: new Headers({
     'Accept': 'application/json',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Authorization': 'Token dfcb272519e02efd76516ee4c8eeb735e65beaae',
   }), 
   body: 'name=novageladeira&obj_type=naoeletrodomestico&new=false&owner=1'
 }).then(function(res) {
    return res.json();
   })
  .then(function(resJson) {
    return resJson;
   })


//get user auth token by other path

var token = ""

var promise = fetch('https://whispering-peak-32557.herokuapp.com/rest-auth/login/', { 
   method: 'post', 
   headers: new Headers({
     'Content-Type': 'application/x-www-form-urlencoded'
   }), 
   body: 'username=admin&password=root'
 }).then(function(res) {
    return res.json();
   })

 promise.then ((key) => token = key.key)
 localStorage.setItem('token' , token)



//register a user 

var res = ""
var a = fetch('https://whispering-peak-32557.herokuapp.com/rest-auth/registration/', { 
   method: 'post', 
   headers: new Headers({
     
     'Content-Type': 'application/x-www-form-urlencoded'
   }), 
   body: 'username=novids&email=asdasdaa@gmail.com&password1=lips1997&password2=lips1997'
 }).then((response) => res = response.json())
  
  a.then((result)=> res = result)


  //register user test with errors


  var res = ""
var a = fetch('https://whispering-peak-32557.herokuapp.com/rest-auth/registration/', { 
   method: 'post', 
   resolveWithFullResponse: true,
   headers: new Headers({
     
     'Content-Type': 'application/x-www-form-urlencoded'
   }), 
   body: 'username=novids&email=asdasdaa@gmail.com&password1=lips1997&password2=lips1997'
 }).then((response) => res = response.json()).catch(function (err) {
        console.log(err)
    });
  
  a.then((result)=> res = result)