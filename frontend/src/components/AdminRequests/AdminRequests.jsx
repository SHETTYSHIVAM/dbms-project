import React, {useEffect, useState} from "react";
import axiosInstance from "../../../axios";
import {toast} from "react-toastify";
import ReservationCard from "./ReservationCard";

const ITEMS_PER_PAGE = 6;

function AdminRequests() {
    const [reservations, setReservations] = useState([]);
    const [filteredReservations, setFilteredReservations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState("pending");
    const [currentPage, setCurrentPage] = useState(1);

    const fetchReservations = async () => {
        try {
            const response = await axiosInstance.get("/reservations/");
            if (response.status === 200) {
                setReservations(response.data);
            } else {
                toast.error("Could not fetch reservations");
            }
        } catch (error) {
            toast.error("Something went wrong. Please try again later.");
            console.error("Error fetching reservations:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchReservations();
    }, []);

    useEffect(() => {
        const filtered = filter === "all"
            ? reservations
            : reservations.filter(
                (res) => res.reservation.status.toLowerCase() === filter
            );
        setFilteredReservations(filtered);
        setCurrentPage(1); // Reset to first page when filter changes
    }, [filter, reservations]);

    const handleApprove = async (id) => {
        try {
            const response = await axiosInstance.post(`/reservations/fulfill/${id}`);
            if (response.status === 201) {
                toast.success("Reservation approved and fulfilled");
                fetchReservations();
            }
        } catch (err) {
            toast.error(err.response?.data?.message || "Approval failed");
        }
    };

    const handleReject = async (id) => {
        const confirm = window.confirm("Are you sure you want to reject this reservation?");
        if (!confirm) return;

        try {
            const response = await axiosInstance.put(`/reservations/${id}`, {
                status: "cancelled",
            });
            if (response.status === 200) {
                toast.success("Reservation rejected");
                fetchReservations();
            }
        } catch (err) {
            toast.error(err.response?.data?.message || "Rejection failed");
        }
    };

    const handleReserve = async (id) => {
        const confirm = window.confirm("Are you sure you want to reserve this book?");
        if (!confirm) return;

        try {
            const response = await axiosInstance.post(`/reservations/${id}`, {
                status: "reserved",
            });
            if (response.status === 200) {
                toast.success("Book reserved");
                fetchReservations();
            }
        } catch (err) {
            toast.error(err.response?.data?.message || "Reservation failed");
        }
    };

    // Pagination logic
    const totalPages = Math.ceil(filteredReservations.length / ITEMS_PER_PAGE);
    const paginatedReservations = filteredReservations.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
    );

    if (loading) return <p className="text-gray-400 px-6">Loading...</p>;

    return (
        <div className="p-6 md:px-12 bg-neutral-950 min-h-screen text-white space-y-8">
            <div className="flex justify-between items-center flex-wrap gap-4">
                <h1 className="text-2xl font-bold">Reservations</h1>
                <select
                    className="bg-zinc-700 text-white px-4 py-2 rounded-lg"
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                >
                    <option value="all">All</option>
                    <option value="pending">Pending</option>
                    <option value="approved">Approved</option>
                    <option value="rejected">Rejected</option>
                </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {paginatedReservations.length > 0 ? (
                    paginatedReservations.map((res) => (
                        <ReservationCard
                            key={res.reservation.id}
                            res={res}
                            onApprove={handleApprove}
                            onReject={handleReject}
                            onReserve={handleReserve}
                        />
                    ))
                ) : (
                    <p className="text-gray-400">No reservations found.</p>
                )}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
                <div className="flex justify-center gap-4 mt-8">
                    <button
                        onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
                        className="px-4 py-2 rounded bg-zinc-700 hover:bg-zinc-600 disabled:opacity-50"
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>
                    <span className="text-lg font-medium">
            Page {currentPage} of {totalPages}
          </span>
                    <button
                        onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
                        className="px-4 py-2 rounded bg-zinc-700 hover:bg-zinc-600 disabled:opacity-50"
                        disabled={currentPage === totalPages}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
}

export default AdminRequests;
