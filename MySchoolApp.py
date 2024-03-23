import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from students.promotion import StudentAllocator

# wide page
st.set_page_config(layout="wide")

class SchoolApp:
    selected_sheets = []
    students_df = None
    students_grid = None

    def render(self):
        self.render_sidebar()
        self.render_main()
    
    def render_sidebar(self):
        with st.sidebar:
            students_file = st.file_uploader("Upload Students file")
            btn_file_upload = st.button("Load")
            if btn_file_upload and students_file:
                xls = pd.ExcelFile(students_file)
                sheets = xls.sheet_names
                if len(sheets) > 1:
                    self.popup_sheet_selection(sheets)
                else:
                    self.selected_sheets = sheets
                for sheet in self.selected_sheets:
                    df = pd.read_excel(students_file, sheet)
                    self.students_df = pd.concat([self.students_df, df])
                self.students_df['RTE'] = self.students_df['RTE'].apply(lambda x:  "RTE" if x == 'RTE' else "General")    
                self.students_df['AcademicBand'] = self.students_df['Percentage'].apply(lambda x: self.__calculate_percentage_group(x))
                self.students_df['Target Section'] = None
    
    def render_main(self):
        tab1, tab2 = st.tabs(["Students", "Analysis"])
        with tab1:
            if self.students_df is not None:
                gd = GridOptionsBuilder.from_dataframe(self.students_df)
                gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
                gd.configure_column("Target Section", editable=True, cellEditor="agSelectCellEditor", cellEditorParams={"values": ['6A', '6B', '6C', '6D', '6E']})
                go = gd.build()
                self.students_grid = AgGrid(self.students_df, gridOptions=go, fit_columns_on_grid_load=True, editable=True)
                cols = st.columns(12)
                with cols[0]:
                    btn_allocate = st.button("Allocate")
                    if btn_allocate:
                        self.students_df['Target Section'] = None
                        allocator = StudentAllocator(self.students_df, ['6A', '6B', '6C', '6D', '6E'])
                        self.students_df = allocator.allocate()
                        st.rerun()
                with cols[1]:
                    btn_save = st.button("Save")
                    if btn_save:
                        self.students_df = self.students_grid['data']
                        st.rerun()



        with tab2:
            if self.students_df is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    dd1 = self.students_df[['Target Section', 'Gender']]
                    fig1 = px.histogram(dd1, x='Target Section', color='Gender', barmode='group', title="Gender distribution", category_orders={"Target Section": ['6A', '6B', '6C', '6D', '6E']})
                    fig1.update_layout(yaxis_title="Student Count", autosize=False, width=400, height=400)
                    st.plotly_chart(fig1, theme="streamlit")

                    dd4 = self.students_df[['Target Section', 'AcademicBand']]
                    fig4 = px.histogram(dd4, x='Target Section', color='AcademicBand', title="Academic distribution", category_orders={"Target Section": ['6A', '6B', '6C', '6D', '6E'], "AcademicBand": ['NA', 5, 6, 7, 8, 9]})
                    fig4.update_layout(yaxis_title="Student Count", autosize=False, width=400, height=400)
                    st.plotly_chart(fig4, theme="streamlit")

                with col2:
                    dd2 = self.students_df[['Target Section', 'House']]
                    fig2 = px.histogram(dd2, x='Target Section', color='House', barmode='group', title="House distribution", category_orders={"Target Section": ['6A', '6B', '6C', '6D', '6E']})
                    fig2.update_layout(yaxis_title="Student Count", autosize=False, width=400, height=400)
                    st.plotly_chart(fig2, theme="streamlit")
                with col3:
                    dd3 = self.students_df[['Target Section', 'RTE']]
                    fig3 = px.histogram(dd3, x='Target Section', color='RTE', barmode='group', title="RTE distribution", category_orders={"Target Section": ['6A', '6B', '6C', '6D', '6E']})
                    fig3.update_layout(yaxis_title="Student Count", autosize=False, width=400, height=400)
                    st.plotly_chart(fig3, theme="streamlit")

    def popup_sheet_selection(self, sheets):
        self.selected_sheets = []
        with st.popover("Select Sheets"):
            for sheet in sheets:
                option = st.checkbox(sheet)
                if option:
                    self.selected_sheets.append(sheet)
    
    def __calculate_percentage_group(self, percentage):
        if isinstance(percentage, float) or isinstance(percentage, int):
            group = int(percentage/10)
            if group < 5:
                group = 5
            return group 
        else:
            return 'NA'

if 'app' not in st.session_state:
    app = SchoolApp()
    st.session_state['app'] = app

app = st.session_state['app']
app.render()
