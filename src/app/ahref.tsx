// app/ahrefKdApi.tsx
import React, { useState } from 'react';

const AhrefKdApi = () => {
  const [keywords, setKeywords] = useState('');

  // Example of using useEffect to make an API call on mount, if needed
  React.useEffect(() => {
    // You can perform API calls or other effects here
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/ahref/kd', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keywords }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      // Handle the data from the response as needed
      console.log(data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="text-center">Ahref Kd Api</h1>
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="keywords-input">
            Insert keywords:
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="keywords-input"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            name="keywords"
            required
          />
        </div>
        <button
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          type="submit"
        >
          Get keywords difficulty
        </button>
      </form>
    </div>
  );
};

export default AhrefKdApi;