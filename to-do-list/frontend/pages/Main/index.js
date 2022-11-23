import React,{useState} from 'react';
import './styles.css';



const Main = () => {

  const [title, setTitle] = useState("To do List")
  const [todoList, setTodoList] = useState([])

  return (
    <div className="principal">
    <div className="container2">
      <b><h1 className='title'>TO-DO LIST - {title}</h1></b>
      <div className="input-group mb-3">
        <input onChange={(event) => setTitle(event.target.value)} value={title} className='form-control' type="text" placeholder='Add your new task'/>
        <button className='input-group-text btn btn-primary rounded-3'>+</button>
        {

        }

      </div>
    </div>
    </div>
  );
}

export default Main;
