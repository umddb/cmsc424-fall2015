#!/bin/bash
echo "Creating application... Press Enter to Continue"
read dummy
rails new blog
cd blog

#bin/rails server

echo "Generating controllers ... Press Enter to Continue"
read dummy
bin/rails generate controller welcome index # "welcome" with "index" action
bin/rails generate controller articles # "articles" controller
bin/rails generate controller Comments

echo "Adding stuff to config/routes.rb... Press Enter to Continue"
read dummy
cat << EOF > config/routes.rb
Rails.application.routes.draw do
  get 'welcome/index'
        root 'welcome#index'
        resources :articles do
                resources :comments
        end

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
bin/rails generate model Article title:string text:text
bin/rails generate model Comment commenter:string body:text article:references

echo "Running rake migrate... Press Enter to Continue"
read dummy
bin/rake db:migrate

cat << EOF > app/views/welcome/index.html.erb
<h1>Hello, Rails!</h1>
<%= link_to 'My Blog', controller: 'articles' %>
EOF

echo "Writing file app/view/articles/show.html.erb"
cat << EOF > app/views/articles/show.html.erb
<p>
  <strong>Title:</strong>
  <%= @article.title %>
</p>
 
<p>
  <strong>Text:</strong>
  <%= @article.text %>
</p>

<h2>Comments</h2>
<% @article.comments.each do |comment| %>
  <p>
    <strong>Commenter:</strong>
    <%= comment.commenter %>
  </p>
 
  <p>
    <strong>Comment:</strong>
    <%= comment.body %>
  </p>
<% end %>
 
<h2>Add a comment:</h2>
<%= form_for([@article, @article.comments.build]) do |f| %>
  <p>
    <%= f.label :commenter %><br>
    <%= f.text_field :commenter %>
  </p>
  <p>
    <%= f.label :body %><br>
    <%= f.text_area :body %>
  </p>
  <p>
    <%= f.submit %>
  </p>
<% end %>
 
<%= link_to 'Edit', edit_article_path(@article) %> |
<%= link_to 'Back', articles_path %>
EOF

echo "Writing file app/view/articles/new.html.erb"
cat << EOF > app/views/articles/new.html.erb
<%= form_for :article, url: articles_path do |f| %>
 
  <% if @article.errors.any? %>
    <div id="error_explanation">
      <h2>
	<%= pluralize(@article.errors.count, "error") %> prohibited
	this article from being saved:
      </h2>
      <ul>
	<% @article.errors.full_messages.each do |msg| %>
	  <li><%= msg %></li>
	<% end %>
      </ul>
    </div>
  <% end %>
 
  <p>
    <%= f.label :title %><br>
    <%= f.text_field :title %>
  </p>
 
  <p>
    <%= f.label :text %><br>
    <%= f.text_area :text %>
  </p>

 
  <p>
    <%= f.submit %>
  </p>
 
<% end %>
 
<%= link_to 'Back', articles_path %>
EOF

echo "Writing file app/view/articles/edit.html.erb"
cat << EOF > app/views/articles/edit.html.erb
<h1>Editing article</h1>

<%= form_for :article, url: article_path(@article), method: :patch do |f| %>
 
  <% if @article.errors.any? %>
    <div id="error_explanation">
      <h2>
	<%= pluralize(@article.errors.count, "error") %> prohibited
	this article from being saved:
      </h2>
      <ul>
	<% @article.errors.full_messages.each do |msg| %>
	  <li><%= msg %></li>
	<% end %>
      </ul>
    </div>
  <% end %>
 
  <p>
    <%= f.label :title %><br>
    <%= f.text_field :title %>
  </p>
 
  <p>
    <%= f.label :text %><br>
    <%= f.text_area :text %>
  </p>

  <p>
    <%= f.submit %>
  </p>
 
<% end %>
 
<%= link_to 'Back', articles_path %>
EOF

echo "Writing file app/views/articles/index.html.erb"
cat << EOF > app/views/articles/index.html.erb
<h1>Listing Articles</h1>
<%= link_to 'New article', new_article_path %>
<table>
  <tr>
  <th>Title</th>
  <th>Text</th>
    <th colspan="2"></th>
  </tr>
 
  <% @articles.each do |article| %>
    <tr>
      <td><%= article.title %></td>
      <td><%= article.text %></td>
      <td><%= link_to 'Show', article_path(article) %></td>
      <td><%= link_to 'Edit', edit_article_path(article) %></td>
      <td><%= link_to 'Destroy', article_path(article),
                    method: :delete,
		    data: { confirm: 'Are you sure?' } %></td>
    </tr>
  <% end %>
</table>
<br>
EOF

echo "Writing file app/controllers/articles_controller.rb"
cat << EOF > app/controllers/articles_controller.rb
class ArticlesController < ApplicationController
  def index
    @articles = Article.all
  end
 
  def show
    @article = Article.find(params[:id])
  end
 
  def new
    @article = Article.new
  end
 
  def edit
    @article = Article.find(params[:id])
  end
 
  def create
    @article = Article.new(article_params)
 
    if @article.save
      redirect_to @article
    else
      render 'new'
    end
  end
 
  def update
    @article = Article.find(params[:id])
 
    if @article.update(article_params)
      redirect_to @article
    else
      render 'edit'
    end
  end
 
  def destroy
    @article = Article.find(params[:id])
    @article.destroy
 
    redirect_to articles_path
  end
 
  private
    def article_params
      params.require(:article).permit(:title, :text)
    end
end
EOF

echo "Writing file app/controllers/comments_controller.rb"
cat << EOF > app/controllers/comments_controller.rb
class CommentsController < ApplicationController
  def create
    @article = Article.find(params[:article_id])
    @comment = @article.comments.create(comment_params)
    redirect_to article_path(@article)
  end
 
  private
    def comment_params
      params.require(:comment).permit(:commenter, :body)
    end
end
EOF

echo "Writing file app/models/article.rb"
cat << EOF > app/models/article.rb
class Article < ActiveRecord::Base
	has_many :comments
	validates :title, presence: true,
	  length: { minimum: 5 }
end
EOF

echo "Writing file app/models/comment.rb"
cat << EOF > app/models/comment.rb
class Comment < ActiveRecord::Base
	belongs_to :article
end
EOF
