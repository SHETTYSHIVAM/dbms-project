import React, {useEffect, useState} from 'react';
import axiosInstance from '../../../axios';
import {FaEdit, FaTimes, FaTrash, FaUpload} from 'react-icons/fa';

const ManageBooks = () => {
    const [books, setBooks] = useState([]);
    const [form, setForm] = useState({
        isbn: '',
        title: '',
        author: '',
        genre: '',
        published_year: '',
        publisher: '',
        image_url: '',
        language: ''
    });
    const [editingIsbn, setEditingIsbn] = useState(null);
    const [csvFile, setCsvFile] = useState(null);

    const token = localStorage.getItem('token');

    useEffect(() => {
        fetchBooks();
    }, []);

    const fetchBooks = async () => {
        try {
            const res = await axiosInstance.get('/books/', {
                headers: {Authorization: `Bearer ${token}`}
            });
            setBooks(res.data);
        } catch (err) {
            console.error('Fetch error:', err);
        }
    };

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = editingIsbn ? `/books/${editingIsbn}` : '/books/';
        const method = editingIsbn ? 'put' : 'post';

        try {
            await axiosInstance[method](url, form, {
                headers: {Authorization: `Bearer ${token}`}
            });
            setForm({
                isbn: '',
                title: '',
                author: '',
                genre: '',
                published_year: '',
                publisher: '',
                image_url: '',
                language: ''
            });
            setEditingIsbn(null);
            fetchBooks();
        } catch (err) {
            console.error('Submit error:', err);
        }
    };

    const handleEdit = (book) => {
        setForm(book);
        setEditingIsbn(book.isbn);
    };

    const handleDelete = async (isbn) => {
        try {
            await axiosInstance.delete(`/books/${isbn}`, {
                headers: {Authorization: `Bearer ${token}`}
            });
            fetchBooks();
        } catch (err) {
            console.error('Delete error:', err);
        }
    };

    const handleCSVUpload = async () => {
        if (!csvFile) return;

        const formData = new FormData();
        formData.append('file', csvFile);

        try {
            await axiosInstance.post('/books/bulk-upload', formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            fetchBooks();
            alert('CSV upload completed');
        } catch (err) {
            console.error('CSV upload error:', err);
            alert('CSV upload failed');
        }
    };

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <h2 className="text-3xl font-semibold mb-4">Manage Books</h2>

            {/* Form */}
            <form onSubmit={handleSubmit}
                  className="grid grid-cols-2 md:grid-cols-3 gap-4 bg-white p-4 rounded shadow mb-6">
                {Object.keys(form).map((field) => (
                    <input
                        key={field}
                        type={field === 'published_year' ? 'number' : 'text'}
                        name={field}
                        placeholder={field.replace('_', ' ')}
                        value={form[field]}
                        onChange={handleChange}
                        required={['isbn', 'title', 'author', 'genre'].includes(field)}
                        disabled={field === 'isbn' && editingIsbn}
                        className="border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                ))}
                <div className="col-span-2 md:col-span-3 flex gap-2">
                    <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                        {editingIsbn ? 'Update' : 'Add'} Book
                    </button>
                    {editingIsbn && (
                        <button
                            type="button"
                            onClick={() => {
                                setForm({
                                    isbn: '',
                                    title: '',
                                    author: '',
                                    genre: '',
                                    published_year: '',
                                    publisher: '',
                                    image_url: '',
                                    language: ''
                                });
                                setEditingIsbn(null);
                            }}
                            className="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded flex items-center gap-1"
                        >
                            <FaTimes/> Cancel
                        </button>
                    )}
        </div>
            </form>

            {/* CSV Upload */}
            <div className="bg-white p-4 rounded shadow mb-6">
                <h3 className="text-xl font-medium mb-2 flex items-center gap-2">
                    <FaUpload/> Bulk Upload via CSV
                </h3>
                <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setCsvFile(e.target.files[0])}
                    className="mb-2"
                />
                <button
                    onClick={handleCSVUpload}
                    disabled={!csvFile}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded disabled:opacity-50"
                >
                    Upload CSV
                </button>
                <p className="text-sm text-gray-600 mt-1">
                    CSV should have headers: <code>Subject,Title,Author,Published Year,Language,Cover
                    URL,Publisher</code>
                </p>
            </div>

            {/* Books Table */}
            <div className="overflow-auto bg-white rounded shadow">
                <table className="w-full text-left border border-gray-300">
                    <thead className="bg-gray-100">
                    <tr>
                        {Object.keys(form).map(field => (
                            <th key={field} className="p-2 border">{field}</th>
                        ))}
                        <th className="p-2 border">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {books.map(book => (
                        <tr key={book.isbn} className="border-t">
                            {Object.keys(form).map(field => (
                                <td key={field} className="p-2 border">{book[field]}</td>
                            ))}
                            <td className="p-2 border flex gap-2">
                                <button onClick={() => handleEdit(book)} className="text-blue-600 hover:text-blue-800">
                                    <FaEdit/>
                                </button>
                                <button onClick={() => handleDelete(book.isbn)}
                                        className="text-red-600 hover:text-red-800">
                                    <FaTrash/>
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ManageBooks;
