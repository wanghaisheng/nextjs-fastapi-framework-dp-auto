import { create } from "zustand"
type Todo = {
  id: number
  title: string
  completed: boolean
}

type CreateTodo = {
  title: string
}

type TodoStore = {
  todos: Todo[]
  fetchTodos: () => void
  addTodo: (todo: CreateTodo) => void
  updateTodo: (updatedTodo: Todo) => void
  deleteTodo: (id: number) => void
}
// Add this to your existing type definitions
// This could be in a types file or at the top of your store file
type AhrefsData = {
  keyword: string
  kd: number
  des: string
}
type AhrefsState = {
  ahrefData: AhrefsData[]
  ahrefError: string | null
  fetchAhrefsData: (keywords: string) => void
}

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:3000/api"

export const useStore = create<TodoStore & AhrefsState>((set) => ({
  ahrefData: [],
  ahrefError: null,

  async fetchAhrefs(keywords: string) {
    try {
      const response = await fetch(`${URL}/api/ahref/kd`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keywords }),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: AhrefsData[] = await response.json()
      set((state) => ({ ahrefData: data }))
    } catch (error) {
      set((state) => ({ ahrefError: error.message }))
    }
  },
  todos: [],
  fetchTodos: async () => {
    try {
      const response = await fetch(`${URL}/todos`)
      const todos = await response.json()
      set({ todos })
    } catch (error) {
      console.error("Error fetching todos:", error)
    }
  },
  addTodo: async (todo) => {
    try {
      const response = await fetch(`${URL}/todos`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(todo),
      })
      const createdTodo = await response.json()
      set((state) => ({ todos: [...state.todos, createdTodo] }))
    } catch (error) {
      console.error("Error creating todo:", error)
    }
  },
  updateTodo: async (updatedTodo) => {
    try {
      const response = await fetch(`${URL}/todos/${updatedTodo.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedTodo),
      })
      const updatedItem = await response.json()
      set((state) => ({
        todos: state.todos.map((todo) =>
          todo.id === updatedItem.id ? updatedItem : todo
        ),
      }))
    } catch (error) {
      console.error("Error updating todo:", error)
    }
  },
  deleteTodo: async (id) => {
    try {
      await fetch(`${URL}/todos/${id}`, {
        method: "DELETE",
      })
      set((state) => ({
        todos: state.todos.filter((todo) => todo.id !== id),
      }))
    } catch (error) {
      console.error("Error deleting todo:", error)
    }
  },
}))
