class CreateInstructors < ActiveRecord::Migration
  def change
    create_table :instructors do |t|
      t.string :name
      t.string :office
      t.string :webpage

      t.timestamps null: false
    end
  end
end
