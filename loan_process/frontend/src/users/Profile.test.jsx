import React from 'react';
import { render, screen } from '@testing-library/react';
import Profile from './Profile';

describe('Profile', () => {
  test('renders Profile component', () => {
    render(<Profile/>);
    expect(screen.getByText(/profile/i)).toBeInTheDocument();
  });
});