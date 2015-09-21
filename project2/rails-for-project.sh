#!/bin/bash
echo "Creating application... Press Enter to Continue"
read dummy
rails new grading
cd grading
# bin/rails server

echo "Generating controllers ... Press Enter to Continue"
read dummy
bin/rails generate controller welcome index 
bin/rails generate controller Instructors 
bin/rails generate controller Students
bin/rails generate controller Courses

echo "Adding stuff to config/routes.rb... Press Enter to Continue"
read dummy
cat << EOF > config/routes.rb
Rails.application.routes.draw do
  get 'welcome/index'
  root 'welcome#index'
  resources :instructors 
  resources :courses
  resources :students

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
  end
EOF

echo "Generating models ... Press Enter to Continue"
read dummy
bin/rails generate model Instructor name:string office:string webpage:string
bin/rails generate model Course title:string description:text
bin/rails generate model Student name:string address:text

echo "Running rake migrate... Press Enter to Continue"
read dummy
bin/rake db:migrate

cat << EOF > app/views/welcome/index.html.erb
<h1>Hello, Rails!</h1>
<%= link_to 'Instructors', controller: 'instructors' %><br><br>
<%= link_to 'Students', controller: 'students' %><br><br>
<%= link_to 'Courses', controller: 'courses' %>
EOF

echo "Writing file app/view/instructors/show.html.erb"
cat << EOF > app/views/instructors/show.html.erb
<p>
<strong>Name:</strong>
<%= @instructor.name %>
</p>

<p>
<strong>Department:</strong>
<%= @instructor.office %>
</p>

<p>
<strong>Webpage:</strong>
<%= @instructor.webpage %>
</p>

The information about assignments available for grading should appear here. <br><br>

A link to creating an assignment should also appear here. <br><br>

<%= link_to 'Edit', edit_instructor_path(@instructor) %> |
<%= link_to 'Back', instructors_path %>
EOF

echo "Writing file app/view/students/show.html.erb"
cat << EOF > app/views/students/show.html.erb
<p>
<strong>Name:</strong>
<%= @student.name %>
</p>

<p>
<strong>Address:</strong>
<%= @student.address %>
</p>

<h3> Available Assignments </h3>
The information about assignments available for submitting (or editing) should appear here.

<h3> Scores for Submitted Assignments </h3>
The information about grades for completed assignments should appear here.

<%= link_to 'Edit', edit_student_path(@student) %> |
<%= link_to 'Back', students_path %>
EOF

echo "Writing file app/view/courses/show.html.erb"
cat << EOF > app/views/courses/show.html.erb
<p>
<strong>Title:</strong>
<%= @course.title %>
</p>

<p>
<strong>Description:</strong>
<%= @course.description %>
</p>

<%= link_to 'Edit', edit_course_path(@course) %> |
<%= link_to 'Back', courses_path %>
EOF

echo "Writing file app/view/instructors/new.html.erb"
cat << EOF > app/views/instructors/new.html.erb
<%= form_for :instructor, url: instructors_path do |f| %>
 
  <% if @instructor.errors.any? %>
    <div id="error_explanation">
      <h2>
	<%= pluralize(@instructor.errors.count, "error") %> prohibited
	this instructor from being saved:
      </h2>
      <ul>
	<% @instructor.errors.full_messages.each do |msg| %>
	  <li><%= msg %></li>
	<% end %>
      </ul>
    </div>
  <% end %>
 
  <p>
    <%= f.label :name %><br>
    <%= f.text_field :name %>
  </p>
 
  <p>
    <%= f.label :office %><br>
    <%= f.text_area :office %>
  </p>

  <p>
    <%= f.label :webpage %><br>
    <%= f.text_area :webpage %>
  </p>
 
  <p>
    <%= f.submit %>
  </p>
 
<% end %>
 
<%= link_to 'Back', instructors_path %>
EOF

echo "Writing file app/view/instructors/edit.html.erb"
cat << EOF > app/views/instructors/edit.html.erb
<h1>Editing article</h1>

<%= form_for :instructor, url: instructor_path(@instructor), method: :patch do |f| %>
 
  <% if @instructor.errors.any? %>
    <div id="error_explanation">
      <h2>
	<%= pluralize(@instructor.errors.count, "error") %> prohibited
	this instructor from being saved:
      </h2>
      <ul>
	<% @instructor.errors.full_messages.each do |msg| %>
	  <li><%= msg %></li>
	<% end %>
      </ul>
    </div>
  <% end %>
 
  <p>
    <%= f.label :name %><br>
    <%= f.text_field :name %>
  </p>
 
  <p>
    <%= f.label :office %><br>
    <%= f.text_area :office %>
  </p>

  <p>
    <%= f.label :webpage %><br>
    <%= f.text_area :webpage %>
  </p>
 
  <p>
    <%= f.submit %>
  </p>
 
<% end %>
 
<%= link_to 'Back', instructors_path %>
EOF

echo "Writing file app/views/courses/new.html.erb"
cat << EOF > app/views/courses/new.html.erb
Use app/views/instructors/new.html.erb as a template to create a similar page for courses (including error detection)
EOF

echo "Writing file app/views/students/new.html.erb"
cat << EOF > app/views/students/new.html.erb:
Use app/views/instructors/new.html.erb as a template to create a similar page for students (including error detection).
EOF

echo "Writing file app/views/instructors/index.html.erb"
cat << EOF > app/views/instructors/index.html.erb
<h1>Listing Instructors</h1>
<table>
  <tr>
    <th>Name</th>
    <th>Office</th>
    <th>Webpage</th>
    <th colspan="2"></th>
  </tr>
 
  <% @instructors.each do |instructor| %>
    <tr>
      <td><%= instructor.name %></td>
      <td><%= instructor.office %></td>
      <td><%= instructor.webpage %></td>
      <td><%= link_to 'Show', instructor_path(instructor) %></td>
      <td><%= link_to 'Edit', edit_instructor_path(instructor) %></td>
      <td><%= link_to 'Destroy', instructor_path(instructor),
                    method: :delete,
		    data: { confirm: 'Are you sure?' } %></td>
    </tr>
  <% end %>
</table>
<br>
<%= link_to 'Create new instructor', new_instructor_path %> <br>
EOF

echo "Writing file app/views/courses/index.html.erb"
cat << EOF > app/views/courses/index.html.erb
Use app/views/instructors/index.html.erb as a template to create a similar page for courses.
EOF

echo "Writing file app/views/students/index.html.erb"
cat << EOF > app/views/students/index.html.erb
Use app/views/instructors/index.html.erb as a template to create a similar page for students.
EOF

echo "Writing file app/controllers/instructors_controller.rb"
cat << EOF > app/controllers/instructors_controller.rb
class InstructorsController < ApplicationController
  def index
    @instructors = Instructor.all
  end
 
  def show
    @instructor = Instructor.find(params[:id])
  end
 
  def new
    @instructor = Instructor.new
  end
 
  def edit
    @instructor = Instructor.find(params[:id])
  end
 
  def create
    @instructor = Instructor.new(instructor_params)
 
    if @instructor.save
      redirect_to @instructor
    else
      render 'new'
    end
  end
 
  def update
    @instructor = Instructor.find(params[:id])
 
    if @instructor.update(instructor_params)
      redirect_to @instructor
    else
      render 'edit'
    end
  end
 
  def destroy
    @instructor = Instructor.find(params[:id])
    @instructor.destroy
 
    redirect_to instructors_path
  end
 
  private
    def instructor_params
      params.require(:instructor).permit(:name, :office, :webpage)
    end
end
EOF

echo "Use app/controllers/instructors_controller.rb as a template to create a similar files for students and courses"
echo "Press Enter to End"
read dummy
