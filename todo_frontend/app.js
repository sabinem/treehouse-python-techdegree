'use strict';

// https://angularjs.de/artikel/angularjs-login-sicherheit
// this is the app
// ngResource is added as a dependency
angular.module('todoListApp', ['ngResource'])

// the main controller    
// login controller: controls whether the user is logged in
// a token for api access is then stored in $window    
.controller('mainCtrl', ['Todo', '$scope', '$http', '$window', function(Todo, $scope, $http, $window){

  $scope.message = "Please login now!";
  // addTodo does not hit the database
  // it just adds new items in the UI and ng-model, 
  // the actual insert into the database occurs only
  // when the save button was hit
  $scope.addTodo = function() {
    var todo = new Todo();
    todo.name = 'New task!';
    todo.completed = false;
    todo.newitem = true;
    $scope.todos.unshift(todo);
  };

  $scope.reloadTodos = function() {
     $scope.todos = Todo.query();
  };
  
    //Login function;
  $scope.Login = function(){
    $http.post('http://127.0.0.1:8000/api/v1/login', $scope.user)
      .then(function (response) {
        $window.sessionStorage.token = 'Token ' + response.data.token;
        $scope.user.status = "Logged in as " + $scope.user.username;
        $scope.user.loggedin = true;
        //$window.sessionStorage.token = '';
        // the query method comes from ngResource
        // it queries the data over the api
        $scope.todos = Todo.query();
        $scope.message = '';
      }, function(error){
        $scope.message = "Sorry, this combination of user and password is unknown!"
      }
    );
  };

  // Logout function
  $scope.Logout = function(){
    console.log('user logout');
    $window.sessionStorage.token = '';
    $scope.user.status = "";
    $scope.user.loggedin = false;
    $scope.user.username = '';
    $scope.user.password = '';
    $scope.todos = Todo.query();
    $scope.message = "Goodbye for now!";
  };
  
}])
    
// controller of the directive for todos
// todos are saved on bulk by the saveTodos method
// they are deleted one by one with thet deleteTodo method
// both these methods make use of ngResource methods
// which are $save and $delete
// $update was custom added in ngResource
.controller('todoCtrl', function($scope, $http, Todo) {

  $scope.deleteTodo = function(todo, index) {
    // the index is cut short of one element
    $scope.todos.splice(index, 1);
    // the resource delete method is called
    todo.$delete();
  };
  
  $scope.saveTodos = function() {
    // bulk save of new and updated todos

    // filtering for todos that have been edited, but not saved to the server
    var filteredTodos = $scope.todos.filter(function(todo){
      if(todo.edited) {
        return todo;
      }
    });
    // for all the edited todos: they are either updated or saved
    filteredTodos.forEach(function(todo) {
      console.log('saving todos');
      if (todo.id) {
        todo.$update();
      } else {
        todo.$save();
      }

    });
  }; 
})
// a factory for the resource of todos is added
// there is a name and a callback
// the callback is executed when

// following methods come with ngResource
// get, query, save, remove, delete
// also there are methods for instances: $save, $delete, $remove
    
.factory('Todo', function($resource){
  return $resource('http://127.0.0.1:8000/api/v1/todos/:id', {id: '@id'}, {
    // the update method has to be defined since it doese not come
    // preconfigured
    update: {
      method: 'PUT'
    }
  });
})

// an Injector for Authentication:
// this is injected before any $http request andd adds an Authorization header
// to the request
.factory('AuthInterceptor', ['$window', '$q', function($window, $q){
  return {
    request: function(confiq) {
      if ($window.sessionStorage.token){
        confiq.headers['Authorization'] = $window.sessionStorage.token;
      }
      return confiq;
    },
    requestError: function(rejection){
      console.log('request error due to', rejection);
      return $q.reject(rejection);
    }
  }
}])
.config(['$httpProvider', function($httpProvider) {
  //$httpProvider.defaults.headers.common['Authorization'] = $window.$window.sessionStorage.token;
  $httpProvider.defaults.headers.common['Content-Type'] = 'application/text';
  $httpProvider.interceptors.push('AuthInterceptor');
  console.log('http configured');
}]);
  
