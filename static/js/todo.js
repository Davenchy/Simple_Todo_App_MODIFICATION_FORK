const todoInputEl = document.getElementById('todo_input')
const todoFormEl = document.getElementById('todo_form')
const todoListEl = document.getElementById('todo_list')
const stateEl = document.getElementById('state')

const endpoint = "/api/todos"
let todoList = []

todoFormEl.addEventListener('submit', (e) => {
    e.preventDefault()
    addTodo(todoInputEl.value)
    todoInputEl.value = ''
})

function setState(state) {
    stateEl.innerText = !state ? '' : state === true ? 'Saving' : state
}

function createTodoElement(todo) {
    const todoEl = document.createElement('div')
    const todoTextEl = document.createElement('h3')
    const deleteBtnEl = document.createElement('span')

    todoEl.classList.add('p-2', 'my-2', 'flex', 'justify-between', 'items-baseline')

    todoTextEl.classList.add('text-black', 'font-bold')
    todoTextEl.innerText = todo.todo

    deleteBtnEl.classList.add('material-symbols-outlined', 'text-red-500', 'hover:bg-gray-300', 'border-sm', "cursor-pointer")
    deleteBtnEl.innerText = 'delete'
    deleteBtnEl.addEventListener('click', () => removeTodo(todo.id))

    todoEl.append(todoTextEl, deleteBtnEl)
    return todoEl
}

function clearTodoListElement() {
    const nodesList = Array.from(todoListEl.childNodes)
    for (var node of nodesList)
        todoListEl.removeChild(node)
}

function renderTodoList() {
    clearTodoListElement()
    for (var todo of todoList)
        todoListEl.append(createTodoElement(todo))
}

async function updateTodoList() {
    setState("Loading")
    const res = await fetch('/api/todos')
    setState()
    if (res.ok)
        todoList = await res.json()
}

async function refreshTodoList() {
    await updateTodoList()
    renderTodoList()
}

async function addTodo(value) {
    setState(true)
    const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            todo: value
        })
    })
    setState()
    if (res.ok) {
        todoList.push(await res.json())
        renderTodoList()
    }
}

async function removeTodo(id) {
    setState(true)
    const res = await fetch(endpoint, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
    })
    setState()
    if (res.ok) {
        todoList = todoList.filter(todo => todo.id !== id)
        renderTodoList()
    }
}

refreshTodoList();
