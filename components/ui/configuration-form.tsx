// import React from 'react';
'use client';
import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';

interface FormData {
  candidate_url: string;
  job_description_url: string;
  minimum_salary: string;
  maximum_salary: string;
}

export default function Configuration() {
  
  const [formData, setFormData] = useState<FormData>({
    candidate_url: '',
    job_description_url: '',
    minimum_salary: '',
    maximum_salary:  '',
  });


  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({ ...prevState, [name]: value }));
  };


  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      console.log(formData)
      await axios.post('http://localhost:5000/new', formData);
    } catch (error) {
      console.error('There was an error sending the data', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>

      <div className="flex space-x-12">
        
        <div className="flex-shrink-0 w-1/3">
          <h2 className="text-base font-semibold leading-7 text-gray-900">
            Start to practice salary negotiation
          </h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Practicing mock interviews for salary negotiation is essential as it helps individuals refine their communication skills, build confidence, and strategically articulate their value and compensation needs, improving the likelihood of securing a desirable salary package.
          </p>
        </div>
        
        <div className="flex-grow space-y-12">
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3">
            <div className="sm:col-span-4">
              <label htmlFor="website" className="block text-sm font-medium leading-6 text-gray-900">
                Candidate Profile
              </label>
              <div className="mt-2">
                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <span className="flex select-none items-center pl-3 text-gray-500 sm:text-sm">http://</span>
                  <input
                    type="text"
                    name="datasource"
                    id="datasource"
                    className="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                    placeholder="www.linkedin.com"
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>
        
            <div className="sm:col-span-4">
              <label htmlFor="website" className="block text-sm font-medium leading-6 text-gray-900">
                Job Description
              </label>
              <div className="mt-2">
                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <span className="flex select-none items-center pl-3 text-gray-500 sm:text-sm">http://</span>
                  <input
                    type="text"
                    name="datasource"
                    id="datasource"
                    className="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                    placeholder="jobs.linkedin.com"
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            <div className="col-span-full">
              <label htmlFor="about" className="block text-sm font-medium leading-6 text-gray-900">
                Minimum Salary
              </label>
              <div className="mt-2">
                <textarea
                  id="about"
                  name="about"
                  rows={2}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  defaultValue={''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="col-span-full">
              <label htmlFor="about" className="block text-sm font-medium leading-6 text-gray-900">
                Maximum Salary
              </label>
              <div className="mt-2">
                <textarea
                  id="about"
                  name="about"
                  rows={2}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  defaultValue={''}
                  onChange={handleChange}
                />
              </div>
            </div>

          </div>

          <div className="mt-6 flex items-center justify-end gap-x-6">
            <button type="button" className="text-sm font-semibold leading-6 text-gray-900">
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-md bg-gray-900 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Start
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}
