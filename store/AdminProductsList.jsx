// src/pages/admin/AdminProductsList.jsx
import React, { useEffect, useState } from "react";
import API from "./api";
import { useNavigate } from "react-router-dom";

export default function AdminProductsList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const fetchProducts = async () => {
    try {
      const res = await API.get("/api/admin/products/");
      setProducts(res.data);
    } catch (err) {
      console.error(err);
      setError("Could not load products.");
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this product?")) return;
    try {
      await API.delete(`/api/admin/products/${id}/`);
      fetchProducts();
    } catch (err) {
      console.error(err);
      setError("Delete failed.");
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold">Products</h2>
        <button onClick={() => navigate("/admin/products/new")} className="bg-rose-500 text-white px-4 py-2 rounded">
          Add Product
        </button>
      </div>

      {error && <div className="text-red-500">{error}</div>}

      <div className="bg-white rounded shadow">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="p-3">Title</th>
              <th className="p-3">Category</th>
              <th className="p-3">Type</th>
              <th className="p-3">Price</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id} className="border-b">
                <td className="p-3">{p.title}</td>
                <td className="p-3">{p.category_name || p.category}</td>
                <td className="p-3">{p.type === "mrp" ? "MRP" : "Dynamic"}</td>
                <td className="p-3">{p.price?.toFixed ? p.price.toFixed(2) : p.price}</td>
                <td className="p-3">
                  <button onClick={() => navigate(`/admin/products/${p.id}/edit`)} className="text-blue-600 mr-3">Edit</button>
                  <button onClick={() => handleDelete(p.id)} className="text-red-600">Delete</button>
                </td>
              </tr>
            ))}
            {products.length === 0 && <tr><td colSpan="5" className="p-4 text-gray-500">No products</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
