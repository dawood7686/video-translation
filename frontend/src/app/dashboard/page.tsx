'use client';

import { useEffect, useState, useCallback } from 'react';
import { api } from '@/lib/api';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';

interface Video {
  id: number;
  title: string;
  target_language: string;
  status: string;
  created_at: string;
  translated_video_url?: string;
  subtitles_url?: string;
}

export default function DashboardPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchVideos = useCallback(async () => {
    try {
      const res = await api.get('/videos/');
      setVideos(res.data);
    } catch (err) {
      console.error('Failed to fetch videos', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    fetchVideos();
  }, [router, fetchVideos]);

  useEffect(() => {
    // ⚡ Bolt Optimization: Only poll when there are videos in a non-terminal state.
    // This eliminates unnecessary network requests and server load when all tasks are complete.
    const hasActiveVideos = videos.some(v => v.status === 'processing' || v.status === 'pending');
    if (!hasActiveVideos) return;

    const interval = setInterval(() => {
      fetchVideos();
    }, 10000);

    return () => clearInterval(interval);
  }, [videos, fetchVideos]);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold leading-6 text-gray-900">Dashboard</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all your translated videos and their current status.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <Link
            href="/dashboard/upload"
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Upload new video
          </Link>
        </div>
      </div>
      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <table className="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">Title</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Target Language</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
                  <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-0">
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="py-4 text-center text-sm text-gray-500">Loading...</td>
                  </tr>
                ) : videos.length === 0 ? (
                   <tr>
                    <td colSpan={5} className="py-4 text-center text-sm text-gray-500">No videos found. Upload one to get started!</td>
                  </tr>
                ) : (
                  videos.map((video) => (
                    <tr key={video.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">
                        {video.title}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{video.target_language.toUpperCase()}</td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm">
                        <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${
                          video.status === 'completed' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                          video.status === 'failed' ? 'bg-red-50 text-red-700 ring-red-600/20' :
                          'bg-yellow-50 text-yellow-800 ring-yellow-600/20'
                        }`}>
                          {video.status}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {new Date(video.created_at).toLocaleDateString()}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                        {video.status === 'completed' && (
                          <div className="flex space-x-4 justify-end">
                            {video.translated_video_url && (
                              <a href={video.translated_video_url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-900">
                                Video
                              </a>
                            )}
                            {video.subtitles_url && (
                              <a href={video.subtitles_url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-900">
                                Subtitles
                              </a>
                            )}
                          </div>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
