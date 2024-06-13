"use client";

import TodoForm from "@/components/TodoForm";
import TodoItem from "@/components/TodoItem";
import { useStore } from "@/store";
import { useEffect } from "react";
import Link from 'next/link'; // Import the Link component

const Home: React.FC = () => {
  const todos = useStore((state) => state.todos);
  const fetchTodos = useStore((state) => state.fetchTodos);
  const { ahrefData, ahrefError, fetchAhrefs } = useStore();

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="container mx-auto max-w-md p-4">
      <TodoForm />
      <h1 className="text-2xl font-bold mb-4">Todo List</h1>
      {todos.length === 0 ? (
        <p className="text-center">No Todos Found</p>
      ) : (
        todos.map((todo) => <TodoItem key={todo.id} todo={todo} />)
      )}
      {/* Link to the new Ahref Kd Api page */}
      <div className="mt-4 text-center">
        <Link href="/ahref" passHref>
          <a className="text-blue-600">Go to Ahref Kd Api</a>
        </Link>
      </div>
    </div>    
  );
};

export default Home;