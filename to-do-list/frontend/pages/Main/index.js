import React,{useState} from 'react';
import './styles.css';



const Main = () => {

  const [inputValue, setInputValue] = useState("")
  const [todoList, setTodoList] = useState([])

  const HandleAddClick = () => {
    setTodoList([...todoList,inputValue])
    setInputValue("")
  }

  return (
    <div className="principal">
    <div className="container2">
      <b><h1 className='title'>TO-DO LIST</h1></b>
      <div className="input-group mb-3">
        <input 
        onChange={(event) => setInputValue(event.target.value)} 
        value={inputValue} 
        className='form-control' 
        type="text" 
        placeholder='Add your new task'/>

        <button onClick={HandleAddClick} className='input-group-text btn btn-primary rounded-3'>+</button>

      </div>

      <div class="tasks">
        <ul className='list-group'>
      {
          todoList.map((task) => <li className='list-group-item post'>{task}<button class="btn-del options">✔</button></li>)
        } 
        </ul>
        </div>
        



    </div>
    </div>
  );
}

export default Main;
