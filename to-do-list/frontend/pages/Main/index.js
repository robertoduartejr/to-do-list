import React, { useState, useEffect } from 'react';
import './styles.css';
import axios from 'axios';


const Main = () => {

  const [inputValue, setInputValue] = useState("")
  const [todoList, setTodoList] = useState([])
  const [name, setName] = useState([])


  useEffect(() => {
    fetch('/users').then(response => response.json().then(data => {
      setName(data.name)
      setTodoList(data.tasks)
    }))
  }, []);

  useEffect(() => {
    console.log(todoList)
    addTask(todoList)
}, [todoList]);


  const addTask = (data) => {
    axios.post('/', data)
      .then(() => {
        console.log("connection ok")
      })
      .catch(() => {
        console.log("conncetion nok")
      })

  }

  const HandleAddClick = () => {

    if (!inputValue.replace(/\s/g, '').length) {
    }
    else {
      setTodoList(todoList => todoList.concat(inputValue));
      setInputValue("");
    }
  }

  const HandleClearClick = () => {
    if (confirm('Are you sure you wanna clear all tasks?')) {
      setTodoList([])
    }
  }

  const HandleDelClick = (index) => {
    if (confirm('Are you sure you finished this task?')) {
      const newTodoList = todoList.filter((_, i) => i !== index);
      setTodoList(newTodoList)
    }
  }
  return (

    <div className="principal">
      <div className="container2">
        <b><h1 className='title'>TO-DO LIST, {name}</h1></b>
        <div className="input-group mb-3">
          <input
            onChange={(event) => setInputValue(event.target.value)}
            value={inputValue}
            className='form-control'
            type="text"
            placeholder='Add your new task' />

          <button onClick={HandleAddClick} className='input-group-text btn btn-primary rounded-3'>+</button>

        </div>

        <div className="tasks">
          <ul className='list-group'>
            {
              todoList.map((task, index) => <li key={index} className='list-group-item post'>{task}<button onClick={() => {
                HandleDelClick(index);
              }} className="btn-del options">✔</button></li>)
            }
          </ul>
        </div>
        <div className="todo-footer">
          You have {todoList.length} pending tasks.

          <button onClick={HandleClearClick} className="input-group-text btn btn-secondary rounded-"> Clear All</button>

        </div>
      </div>
    </div>
  );
}

export default Main;
