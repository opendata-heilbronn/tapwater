package de.opendatahn.tapwater.entity;


import org.springframework.data.annotation.CreatedDate;

import javax.persistence.*;
import java.util.Calendar;

@Entity
public class City {

	@Id
	@GeneratedValue
	private Long id;

	@Column(nullable = false)
	private String name;

	@CreatedDate
	private Calendar createData;

	public Calendar getCreateData() {
		return createData;
	}

	public void setCreateData(Calendar createData) {
		this.createData = createData;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}
}
