import {FaBookmark, FaCalendarAlt, FaCheckCircle, FaEnvelope, FaTimesCircle, FaUser,} from 'react-icons/fa';

function ReservationCard({res, onApprove, onReject, onReserve}) {
    const statusColor = {
        approved: "bg-green-100 text-green-800",
        pending: "bg-yellow-100 text-yellow-800",
        rejected: "bg-red-100 text-red-800",
    };

    return (
        <div
            className="rounded-2xl shadow-md p-6 m-4 bg-white dark:bg-zinc-800 transition duration-300 max-w-md w-full">
            <div className="flex items-center gap-4 mb-4">
                <div
                    className="w-12 h-12 bg-zinc-300 dark:bg-zinc-600 rounded-full flex items-center justify-center text-white text-lg font-bold">
                    {res.user?.name?.charAt(0).toUpperCase() || "?"}
                </div>
                <div>
                    <h2 className="text-xl font-semibold text-zinc-800 dark:text-white">{res.book?.title || "Unknown Title"}</h2>
                    <div
                        className={`inline-block mt-1 text-sm px-2 py-1 rounded-full font-medium ${statusColor[res.reservation.status.toLowerCase()] || "bg-gray-200 text-gray-800"}`}>
                        {res.reservation.status}
                    </div>
                </div>
            </div>

            <div className="text-zinc-600 dark:text-zinc-300 space-y-2">
                <p className="flex items-center gap-2">
                    <FaUser className="text-zinc-400"/>
                    {res.user?.name || "Unknown User"}
                </p>
                <p className="flex items-center gap-2">
                    <FaEnvelope className="text-zinc-400"/>
                    {res.user?.email || "Unknown Email"}
                </p>
                <p className="flex items-center gap-2">
                    <FaCalendarAlt className="text-zinc-400"/>
                    {new Date(res.reservation.reservation_date).toLocaleDateString()}
                </p>
            </div>

            <div className="mt-5 flex flex-wrap gap-3">
                <button
                    onClick={() => onApprove(res.reservation.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                >
                    <FaCheckCircle/> Borrow
                </button>
                <button
                    onClick={() => onReject(res.reservation.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                >
                    <FaTimesCircle/> Reject
                </button>
                <button
                    onClick={() => onReserve(res.reservation.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                    <FaBookmark/> Reserve
                </button>
            </div>
        </div>
    );
}

export default ReservationCard;