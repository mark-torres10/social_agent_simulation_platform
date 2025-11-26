'use client';

import { useState } from 'react';
import { Agent, Post, AgentAction } from '@/types';
import PostCard from './PostCard';

interface AgentDetailProps {
  agent: Agent;
  feed: Post[];
  actions: AgentAction[];
  allPosts: Post[];
}

export default function AgentDetail({
  agent,
  feed,
  actions,
  allPosts,
}: AgentDetailProps) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    metadata: false,
    feed: false,
    likes: false,
    comments: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const likedPosts = actions
    .filter((a) => a.type === 'like' && a.postUri)
    .map((a) => allPosts.find((p) => p.uri === a.postUri))
    .filter((p): p is Post => p !== undefined);

  const comments = actions.filter((a) => a.type === 'comment');

  return (
    <div className="bg-white border border-beige-300 rounded-lg p-4 space-y-3">
      <div className="font-medium text-beige-900">{agent.name}</div>
      <div className="text-sm text-beige-600">{agent.handle}</div>

      {/* Metadata Section */}
      <div>
        <button
          type="button"
          onClick={() => toggleSection('metadata')}
          className="w-full text-left flex items-center justify-between p-2 hover:bg-beige-100 rounded transition-colors"
        >
          <span className="text-sm font-medium text-beige-800">Agent Metadata</span>
          <span className="text-beige-600">
            {expandedSections.metadata ? '▼' : '▶'}
          </span>
        </button>
        {expandedSections.metadata && (
          <div className="mt-2 p-3 bg-beige-50 rounded space-y-2 text-sm">
            <div>
              <span className="font-medium text-beige-800">Name:</span>{' '}
              <span className="text-beige-900">{agent.name}</span>
            </div>
            <div>
              <span className="font-medium text-beige-800">Bio:</span>{' '}
              <span className="text-beige-900">{agent.bio}</span>
            </div>
            <div>
              <span className="font-medium text-beige-800">Generated Bio:</span>{' '}
              <span className="text-beige-900">{agent.generatedBio}</span>
            </div>
            <div>
              <span className="font-medium text-beige-800">Followers:</span>{' '}
              <span className="text-beige-900">{agent.followers.toLocaleString()}</span>
            </div>
            <div>
              <span className="font-medium text-beige-800">Following:</span>{' '}
              <span className="text-beige-900">{agent.following.toLocaleString()}</span>
            </div>
            <div>
              <span className="font-medium text-beige-800">Posts:</span>{' '}
              <span className="text-beige-900">{agent.postsCount.toLocaleString()}</span>
            </div>
          </div>
        )}
      </div>

      {/* Feed Section */}
      <div>
        <button
          type="button"
          onClick={() => toggleSection('feed')}
          className="w-full text-left flex items-center justify-between p-2 hover:bg-beige-100 rounded transition-colors"
        >
          <span className="text-sm font-medium text-beige-800">
            Feed ({feed.length} posts)
          </span>
          <span className="text-beige-600">{expandedSections.feed ? '▼' : '▶'}</span>
        </button>
        {expandedSections.feed && (
          <div className="mt-2 space-y-3">
            {feed.map((post) => (
              <PostCard key={post.uri} post={post} />
            ))}
          </div>
        )}
      </div>

      {/* Liked Posts Section */}
      <div>
        <button
          type="button"
          onClick={() => toggleSection('likes')}
          className="w-full text-left flex items-center justify-between p-2 hover:bg-beige-100 rounded transition-colors"
        >
          <span className="text-sm font-medium text-beige-800">
            Liked Posts ({likedPosts.length})
          </span>
          <span className="text-beige-600">{expandedSections.likes ? '▼' : '▶'}</span>
        </button>
        {expandedSections.likes && (
          <div className="mt-2 space-y-3">
            {likedPosts.length > 0 ? (
              likedPosts.map((post) => <PostCard key={post.uri} post={post} />)
            ) : (
              <div className="p-3 text-sm text-beige-600 bg-beige-50 rounded">
                No liked posts
              </div>
            )}
          </div>
        )}
      </div>

      {/* Comments Section */}
      <div>
        <button
          type="button"
          onClick={() => toggleSection('comments')}
          className="w-full text-left flex items-center justify-between p-2 hover:bg-beige-100 rounded transition-colors"
        >
          <span className="text-sm font-medium text-beige-800">
            Comments ({comments.length})
          </span>
          <span className="text-beige-600">
            {expandedSections.comments ? '▼' : '▶'}
          </span>
        </button>
        {expandedSections.comments && (
          <div className="mt-2 space-y-2">
            {comments.length > 0 ? (
              comments.map((action) => (
                <div
                  key={action.actionId}
                  className="p-3 bg-beige-50 rounded text-sm text-beige-900"
                >
                  Comment on post: {action.postUri}
                </div>
              ))
            ) : (
              <div className="p-3 text-sm text-beige-600 bg-beige-50 rounded">
                No comments
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

