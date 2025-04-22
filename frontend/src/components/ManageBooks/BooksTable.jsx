import React from "react";
import { FaPen } from "react-icons/fa";

const TABLE_HEAD = ["Transaction", "Amount", "Date", "Status", "Account", ""];

const TABLE_ROWS = [
  {
    img: "https://docs.material-tailwind.com/img/logos/logo-spotify.svg",
    name: "Spotify",
    amount: "$2,500",
    date: "Wed 3:00pm",
    status: "paid",
    account: "visa",
    accountNumber: "1234",
    expiry: "06/2026",
  },
  // Add more rows as needed
];

export function BooksTable() {
  return (
    <div className="overflow-x-auto">
      <table className="w-full table-auto text-left border-collapse">
        <thead>
          <tr className="border-b dark:border-zinc-700">
            {TABLE_HEAD.map((head) => (
              <th
                key={head}
                className="px-4 py-3 text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-300"
              >
                {head}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {TABLE_ROWS.map((row) => {
            const {
              img,
              name,
              amount,
              date,
              status,
              account,
              accountNumber,
              expiry,
            } = row;
            return (
              <tr
                key={name}
                className="border-b dark:border-zinc-700 hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors"
              >
                <td className="px-4 py-3 flex items-center gap-3">
                  <img
                    src={img}
                    alt={name}
                    className="h-8 w-8 rounded-full border object-contain p-1"
                  />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-100">
                    {name}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-300">
                  {amount}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-300">
                  {date}
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded-full px-2 py-1 text-xs font-medium capitalize ${
                      status === "paid"
                        ? "bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200"
                        : status === "pending"
                        ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-800 dark:text-yellow-200"
                        : "bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200"
                    }`}
                  >
                    {status}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-3">
                    <img
                      src={
                        account === "visa"
                          ? "https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/logos/visa.png"
                          : "https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/logos/mastercard.png"
                      }
                      alt={account}
                      className="h-6 w-10 object-contain"
                    />
                    <div className="text-sm">
                      <div className="text-gray-700 dark:text-gray-200 capitalize">
                        {account} {accountNumber}
                      </div>
                      <div className="text-xs text-gray-400 dark:text-gray-400">
                        {expiry}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <button className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
                    <FaPen className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="flex justify-between items-center pt-6 border-t mt-4 dark:border-zinc-600">
        <button className="rounded border px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 dark:border-gray-400 dark:text-gray-300 dark:hover:bg-zinc-600">
          Previous
        </button>
        <div className="flex items-center gap-2">
          {[1, 2, 3, "...", 8, 9, 10].map((page, idx) => (
            <button
              key={idx}
              className={`px-3 py-1 text-sm rounded font-medium ${
                page === 1
                  ? "bg-gray-300 text-gray-800 dark:bg-zinc-700 dark:text-white"
                  : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-zinc-800"
              }`}
            >
              {page}
            </button>
          ))}
        </div>
        <button className="rounded border px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 dark:border-gray-400 dark:text-gray-300 dark:hover:bg-zinc-600">
          Next
        </button>
      </div>
    </div>
  );
}
