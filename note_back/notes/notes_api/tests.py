import json

from graphene_django.utils.testing import GraphQLTestCase

# Create your tests here.
class NotesApiTests(GraphQLTestCase):
    def setUp(self):
        response = self.query(
            '''
            mutation{
                register(username:"testuser", email:"testuser@gmail.com", password1:"test1234@",password2:"test1234@"){
                    token,
                    errors,
                    success
                }
            }
            '''
        )
        content = json.loads(response.content)
        self.token = content["data"]["register"]["token"]
        create_note_res = self.create_note(title = "test note", content = "test note", token = self.token)
        self.note_id = json.loads(create_note_res.content)["data"]["createNote"]["note"]["id"]
        
    def get_notes(self, token = None, contains = "", order_by = "-created_at"):
        return self.query(
            '''
            query notes($search:String, $orderBy:String){
                notes(search:$search, orderBy:$orderBy){
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            ''',
            variables={
                "search":contains, 
                "orderBy":order_by,
                },
            headers= {"HTTP_AUTHORIZATION":f"JWT {token}"}
        )
    
    def get_note(self, id, token = None):
        return self.query(
            '''
            query note($id:ID!){
                note(id:$id){
                    id
                }
            }
            ''',
            variables={"id":id},
            headers= {"HTTP_AUTHORIZATION":f"JWT {token}"}
        )    
    
    def create_note(self, title = "", content = "", token = None):
        return self.query(
            '''
            mutation createNote($title:String, $content:String){
                createNote(title:$title, content:$content){
                    note{
                        id
                    }
                }
            }
            ''',
            headers = {"HTTP_AUTHORIZATION":f"JWT {token}"},
            variables = {
                "title":title,
                "content":content,
            }
        ) 
    
    def update_note(self, id, title = "", content = "", token = None):
        return self.query(
            '''
            mutation UpdateNote($id: ID!, $title:String, $content:String) {
                updateNote(id: $id, title: $title, content: $content) {
                    note {
                        id
                    }
                }
            }
            ''',
            variables={
                "id":id,
                "title":title,
                "content":content,
                },
            headers={"HTTP_AUTHORIZATION":f"JWT {token}"}
        ) 
    
    def delete_note(self, id, token = None):
        return self.query(
            '''
            mutation deleteNote($id: ID!){
                deleteNote(id: $id) {
                    message
                }
            }
            ''',
            variables={"id":id,},
            headers={"HTTP_AUTHORIZATION":f"JWT {token}"}
        )            
    
    def test_check_user_not_authenticated_can_not_see_the_notes(self):
        response = self.get_notes()
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["data"]["notes"], None)
        self.assertEqual(content["errors"][0]["message"], "Permission Denied.")
    
    def test_check_user_authenticated_can_see_the_notes(self):
        response = self.get_notes(token=self.token)
        self.assertResponseNoErrors(response)
        
    def test_check_user_not_authenticated_can_not_see_especific_note(self):
        response = self.get_note(id = self.note_id)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["data"]["note"], None)
        self.assertEqual(content["errors"][0]["message"], "Permission Denied.")
    
    def test_check_user_authenticated_can_see_especific_note(self):
        response = self.get_note(id = self.note_id, token=self.token)
        self.assertResponseNoErrors(response)
    
    def test_check_user_not_authenticated_can_not_create_notes(self):
        response = self.create_note(title = "Hello World", content = "Hello World")
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["data"]["createNote"], None)
        self.assertEqual(content["errors"][0]["message"], "Permission Denied.")
    
    def test_check_user_authenticated_can_create_notes(self):
        response = self.create_note(title = "Hello World", content = "Hello World", token = self.token)           
        self.assertResponseNoErrors(response)
    
    def test_check_user_not_authenticated_can_not_edit_notes(self):
        response = self.update_note(id = self.note_id, title = "test edit", content = "test edit")
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["errors"][0]["message"], "Permission Denied.")
        self.assertEqual(content["data"]["updateNote"], None)    
    
    def test_check_user_authenticated_can_edit_notes(self):
        response = self.update_note(id = self.note_id, title = "test edit", content = "test edit", token = self.token)
        self.assertResponseNoErrors(response)
    
    def test_check_user_not_authenticated_can_not_delete_notes(self):
        response = self.delete_note(id = self.note_id)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["errors"][0]["message"], "Permission Denied.")
    
    def test_check_user_authenticated_can_delete_notes(self):
        response = self.delete_note(id = self.note_id, token = self.token)
        self.assertResponseNoErrors(response)
        
    def test_check_raise_invalid_id_when_incorrect_id_is_given(self):
        response = self.delete_note(id = "asd", token = self.token)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)  
        self.assertEqual(content["errors"][0]["message"], "The given id is not valid") 
    
    def test_check_filters_for_notes_work_well(self):
        response = self.get_notes(token = self.token, contains = "test", order_by = "created_at")
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)  
        self.assertEqual(len(content["data"]["notes"]["edges"]) > 0, True)     