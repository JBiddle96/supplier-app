import marimo

__generated_with = "0.3.3"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        update,
        text,
        delete,
        insert,
        select,
    )
    import pandas as pd
    import os
    from dotenv import load_dotenv

    pd.options.mode.copy_on_write = True
    return (
        MetaData,
        Table,
        create_engine,
        delete,
        insert,
        load_dotenv,
        mo,
        os,
        pd,
        select,
        text,
        update,
    )


@app.cell
def __(mo):
    mo.md(f"# PII Supplier Masking {mo.icon('bxs:mask', size=40)}")
    return


@app.cell
def __(MetaData, Table, create_engine, load_dotenv, mo, os, pd, select):
    load_dotenv()
    SERVER = os.getenv("SERVER")
    PORT = os.getenv("PORT")
    DATABASE = os.getenv("DATABASE")
    USERNAME = os.getenv("MSSQL_USERNAME")
    PASSWORD = os.getenv("MSSQL_PASSWORD")
    MASKING_TABLE = os.getenv("MASKING_TABLE")
    ID_TABLE = os.getenv("SUPPLIER_ID_TABLE")
    TYPE_TABLE = os.getenv("SUPPLIER_TYPE_ID_TABLE")

    OPTIONS_COLS = [
        "Address",
        "Phone",
        "Postcode",
        "Email",
    ]

    e = create_engine(
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}?"
        "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )


    def load_supplier_ids():
        with e.connect() as conn:
            df = pd.read_sql(ID_TABLE, conn)
        return df


    supplier_id_df = load_supplier_ids()


    def load_supplier_type_ids():
        with e.connect() as conn:
            df = pd.read_sql(TYPE_TABLE, conn)
        return df


    supplier_type_id_df = load_supplier_type_ids()


    def load_defaults():
        metadata = MetaData()
        table = Table(MASKING_TABLE, metadata, autoload_with=e)
        stmt = select(table).where(table.c.SupplierID == None)
        with e.connect() as conn:
            res = conn.execute(stmt).fetchall()

        defaults = {r[1]: list(r[2:]) for r in res}
        return defaults


    default_masks = load_defaults()


    def load_data():
        with e.connect() as conn:
            df = pd.read_sql(MASKING_TABLE, conn)

        df = df[df["SupplierID"].notna()]
        df["SupplierID"] = df["SupplierID"].astype(int)

        df = df.merge(
            supplier_id_df[["SupplierID", "SupplierName"]],
            on="SupplierID",
            how="left",
            validate="one_to_one",
        )

        df = df.merge(
            supplier_type_id_df,
            on="SupplierTypeID",
            how="left",
        )

        cols = [
            "SupplierID",
            "SupplierName",
            "SupplierTypeID",
            "SupplierType",
        ] + OPTIONS_COLS
        df = df[cols]
        return df


    get_df, set_df = mo.state(load_data())
    return (
        DATABASE,
        ID_TABLE,
        MASKING_TABLE,
        OPTIONS_COLS,
        PASSWORD,
        PORT,
        SERVER,
        TYPE_TABLE,
        USERNAME,
        default_masks,
        e,
        get_df,
        load_data,
        load_defaults,
        load_supplier_ids,
        load_supplier_type_ids,
        set_df,
        supplier_id_df,
        supplier_type_id_df,
    )


@app.cell
def __(get_df):
    df = get_df()
    df
    return df,


@app.cell
def __(df, mo):
    supplier_names = df["SupplierName"]
    supplier_ids = df["SupplierID"]
    supplier_options = {
        f"{name} - {_id}": _id for name, _id in zip(supplier_names, supplier_ids)
    }
    supplier_edit_select = mo.ui.dropdown(options=supplier_options, label="Select supplier")
    return (
        supplier_edit_select,
        supplier_ids,
        supplier_names,
        supplier_options,
    )


@app.cell
def __(
    MASKING_TABLE,
    MetaData,
    OPTIONS_COLS,
    Table,
    df,
    e,
    load_data,
    mo,
    pd,
    set_df,
    supplier_edit_select,
    update,
):
    def submit_edit(values):
        sql_values = {val: 1 if val in values else 0 for val in OPTIONS_COLS}
        old_vals = df.loc[
            df["SupplierID"] == supplier_edit_select.value, OPTIONS_COLS
        ].iloc[0]
        if list(sql_values.values()) == list(old_vals):
            return

        metadata = MetaData()
        table = Table(MASKING_TABLE, metadata, autoload_with=e)
        stmt = (
            update(table)
            .where(table.c["SupplierID"] == supplier_edit_select.value)
            .values(**sql_values)
        )
        with e.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        set_df(load_data())


    def get_multiselect_params():
        selection = df[df["SupplierID"] == supplier_edit_select.value][OPTIONS_COLS]
        if not selection.empty:
            selection = selection.iloc[0]
        else:
            selection = pd.Series()

        options = [o for o in selection.index]
        values = [o for o, val in zip(options, selection) if val]
        return options, values


    options, values = get_multiselect_params()

    bool_select = mo.ui.multiselect(
        options=options, value=values, label="Select fields"
    ).form(
        submit_button_tooltip="Submit change to database",
        on_change=submit_edit,
    )
    edit_tab = mo.vstack([supplier_edit_select, bool_select])
    return (
        bool_select,
        edit_tab,
        get_multiselect_params,
        options,
        submit_edit,
        values,
    )


@app.cell
def __(
    MASKING_TABLE,
    MetaData,
    Table,
    delete,
    e,
    load_data,
    mo,
    set_df,
    supplier_options,
):
    def submit_delete(values): 
        if not values:
            return

        metadata = MetaData()
        table = Table(MASKING_TABLE, metadata, autoload_with=e)
        stmt = (
            delete(table)
            .where(table.c["SupplierID"].in_(supplier_delete_select.value))
        )
        with e.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        set_df(load_data())

    supplier_delete_select = mo.ui.multiselect(
        options=supplier_options, label="Select suppliers to remove"
    ).form(
        submit_button_tooltip="Remove selected suppliers from masking table",
        on_change=submit_delete,
    )
    delete_tab = mo.vstack([supplier_delete_select])
    return delete_tab, submit_delete, supplier_delete_select


@app.cell
def __(
    MASKING_TABLE,
    MetaData,
    OPTIONS_COLS,
    Table,
    default_masks,
    df,
    e,
    insert,
    load_data,
    mo,
    set_df,
    supplier_id_df,
):
    def submit_add(values):
        if not values:
            return

        supplier_types = supplier_id_df.loc[
            supplier_id_df["SupplierID"].isin(values)
        ][["SupplierID", "SupplierTypeID"]]

        metadata = MetaData()
        table = Table(MASKING_TABLE, metadata, autoload_with=e)
        stmt = insert(table)

        params = []
        for val in values:
            print(
                supplier_types.loc[supplier_types["SupplierID"] == val][
                    "SupplierTypeID"
                ]
            )
            type_id = supplier_types.loc[supplier_types["SupplierID"] == val][
                "SupplierTypeID"
            ].iloc[0]
            param = {"SupplierID": val, "SupplierTypeID": int(type_id)}
            param.update(
                {
                    opt: mask
                    for opt, mask in zip(OPTIONS_COLS, default_masks[type_id])
                }
            )
            params.append(param)

        with e.connect() as conn:
            conn.execute(stmt, params)
            conn.commit()

        set_df(load_data())


    def available_suppliers():
        in_mask = set(df["SupplierID"])
        supplier_ids = set(supplier_id_df["SupplierID"])
        available = list(supplier_ids - in_mask)
        available.sort()
        available_df = supplier_id_df.loc[
            supplier_id_df["SupplierID"].isin(available)
        ]
        options = {
            f"{name} - {_id}": _id
            for name, _id in zip(
                available_df["SupplierName"], available_df["SupplierID"]
            )
        }
        return options


    available_options = available_suppliers()
    supplier_add_select = mo.ui.multiselect(
        options=available_options, label="Select suppliers to add"
    ).form(
        submit_button_tooltip="Add selected suppliers to masking table",
        on_change=submit_add,
    )
    add_tab = mo.vstack([supplier_add_select])
    return (
        add_tab,
        available_options,
        available_suppliers,
        submit_add,
        supplier_add_select,
    )


@app.cell
def __(add_tab, delete_tab, edit_tab, mo):
    tabs = mo.ui.tabs({"Edit": edit_tab, "Add":add_tab,"Delete": delete_tab})
    tabs
    return tabs,


if __name__ == "__main__":
    app.run()
